# -*- coding: utf-8 -*-
# @Time    : 2023/10/18 下午10:46
# @Author  : sudoskys
# @File    : __init__.py.py
# @Software: PyCharm
import atexit
import os
import ssl
from typing import List

import hikari
from aio_pika.abc import AbstractIncomingMessage
from hikari.impl import ProxySettings
from loguru import logger
from telebot import formatting

from llmkira.middleware.chain_box import Chain, ChainReloader
from llmkira.middleware.env_virtual import EnvManager
from llmkira.middleware.llm_task import OpenaiMiddleware
from llmkira.receiver import function
from llmkira.receiver.schema import ReplyRunner
from llmkira.schema import RawMessage
from llmkira.sdk.endpoint import openai
from llmkira.sdk.error import RateLimitError
from llmkira.sdk.func_calling.register import ToolRegister
from llmkira.sdk.schema import File, Message
from llmkira.setting.discord import BotSetting
from llmkira.task import Task, TaskHeader
from llmkira.utils import sync

__receiver__ = "discord_hikari"

from llmkira.middleware.router.schema import router_set
from llmkira.transducer import TransferManager

router_set(role="receiver", name=__receiver__)

discord_rest: hikari.RESTApp = hikari.RESTApp(
    proxy_settings=ProxySettings(
        url=BotSetting.proxy_address
    )
)


class DiscordSender(ReplyRunner):
    """
    平台路由
    """

    def __init__(self):
        self.bot = None

    def acquire(self):
        self.bot: hikari.impl.RESTClientImpl = discord_rest.acquire(
            token=BotSetting.token,
            token_type=hikari.TokenType.BOT
        )

    async def file_forward(self, receiver: TaskHeader.Location, file_list: List[File], **kwargs):
        for file_obj in file_list:
            # URL FIRST
            if file_obj.file_url:
                async with self.bot as client:
                    client: hikari.impl.RESTClientImpl
                    _reply = None
                    if receiver.thread_id != receiver.chat_id:
                        _reply = await client.fetch_message(
                            channel=receiver.thread_id,
                            message=receiver.message_id
                        )
                    await client.create_message(
                        channel=receiver.thread_id,
                        attachment=hikari.files.URL(file_obj.file_url, filename=file_obj.file_name),
                        reply=_reply,
                    )
                break
            # DATA
            _data: File.Data = sync(RawMessage.download_file(file_obj.file_id))
            if not _data:
                logger.error(f"file download failed {file_obj.file_id}")
                continue
            file_warp = hikari.files.Bytes(_data.file_data, file_obj.file_name, mimetype="image/png")
            if file_obj.file_name.endswith((".jpg", ".png")):
                async with self.bot as client:
                    client: hikari.impl.RESTClientImpl
                    _reply = None
                    if receiver.thread_id != receiver.chat_id:
                        _reply = await client.fetch_message(
                            channel=receiver.thread_id,
                            message=receiver.message_id
                        )
                    await client.create_message(
                        channel=receiver.thread_id,
                        embed=hikari.EmbedImage(
                            resource=file_warp,
                        ),
                        reply=_reply
                    )
            else:
                async with self.bot as client:
                    client: hikari.impl.RESTClientImpl
                    _reply = None
                    if receiver.thread_id != receiver.chat_id:
                        _reply = await client.fetch_message(
                            channel=receiver.thread_id,
                            message=receiver.message_id
                        )
                    await client.create_message(
                        channel=receiver.thread_id,
                        attachment=file_warp,
                        reply=_reply
                    )

    async def forward(self, receiver: TaskHeader.Location, message: List[RawMessage], **kwargs):
        """
        插件专用转发，是Task通用类型
        """
        for item in message:
            await self.file_forward(
                receiver=receiver,
                file_list=item.file
            )
            async with self.bot as client:
                client: hikari.impl.RESTClientImpl
                _reply = None
                if receiver.thread_id != receiver.chat_id:
                    _reply = await client.fetch_message(
                        channel=receiver.thread_id,
                        message=receiver.message_id
                    )
                await client.create_message(
                    channel=receiver.thread_id,
                    content=item.text,
                    reply=_reply
                )

    async def reply(self, receiver: TaskHeader.Location, message: List[Message], **kwargs):
        """
        模型直转发，Message是Openai的类型
        """
        for item in message:
            _transfer = TransferManager().receiver_builder(agent_name=__receiver__)
            just_file, file_list = _transfer().build(message=item)
            await self.file_forward(
                receiver=receiver,
                file_list=file_list
            )
            if just_file:
                return None
            assert item.content, f"message content is empty"
            async with self.bot as client:
                client: hikari.impl.RESTClientImpl
                _reply = None
                if receiver.thread_id != receiver.chat_id:
                    _reply = await client.fetch_message(
                        channel=receiver.thread_id,
                        message=receiver.message_id
                    )
                await client.create_message(
                    channel=receiver.thread_id,
                    content=item.content,
                    reply=_reply
                )

    async def error(self, receiver: TaskHeader.Location, text, **kwargs):
        async with self.bot as client:
            client: hikari.impl.RESTClientImpl
            _reply = None
            if receiver.thread_id != receiver.chat_id:
                _reply = await client.fetch_message(
                    channel=receiver.thread_id,
                    message=receiver.message_id
                )
            await client.create_message(
                channel=receiver.thread_id,
                content=text,
                reply=_reply
            )

    async def function(self, receiver: TaskHeader.Location,
                       task: TaskHeader,
                       llm: OpenaiMiddleware,
                       result: openai.OpenaiResult,
                       message: Message,
                       **kwargs
                       ):
        if not message.function_call:
            raise ValueError("message not have function_call,forward type error")

        # 获取设置查看是否静音
        _tool = ToolRegister().get_tool(message.function_call.name)
        if not _tool:
            logger.warning(f"not found function {message.function_call.name}")
            return None

        tool = _tool()

        _func_tips = [
            formatting.mbold("🦴 Task be created:") + f" `{message.function_call.name}` ",
            f"""```json\n{message.function_call.arguments}```""",
        ]

        if tool.env_required:
            __secret__ = await EnvManager.from_uid(
                uid=task.receiver.uid
            ).get_env_list(name_list=tool.env_required)
            # 查找是否有空
            _required_env = [
                name
                for name in tool.env_required
                if not __secret__.get(name, None)
            ]
            _need_env_list = [
                f"`{formatting.escape_markdown(name)}`"
                for name in _required_env
            ]
            _need_env_str = ",".join(_need_env_list)
            _func_tips.append(formatting.mbold("🦴 Env required:") + f" {_need_env_str} ")
            help_docs = tool.env_help_docs(_required_env)
            _func_tips.append(formatting.mitalic(help_docs))

        task_message = formatting.format_text(
            *_func_tips,
            separator="\n"
        )

        if not tool.silent:
            async with self.bot as client:
                client: hikari.impl.RESTClientImpl
                _reply = None
                if receiver.thread_id != receiver.chat_id:
                    _reply = await client.fetch_message(
                        channel=receiver.thread_id,
                        message=receiver.message_id
                    )
                await client.create_message(
                    channel=receiver.thread_id,
                    content=task_message,
                    reply=_reply
                )

        # 回写创建消息
        # sign = f"<{task.task_meta.sign_as[0] + 1}>"
        # 二周目消息不回写，因为写过了
        llm.write_back(
            role="assistant",
            name=message.function_call.name,
            message_list=[
                RawMessage(
                    text=f"Okay,Task be created:{message.function_call.arguments}.")]
        )

        # 构建对应的消息
        receiver = task.receiver.copy()
        receiver.platform = __receiver__

        # 运行函数
        await Task(queue=function.__receiver__).send_task(
            task=TaskHeader.from_function(
                parent_call=result,
                task_meta=task.task_meta,
                receiver=receiver,
                message=task.message
            )
        )


__sender__ = DiscordSender()


class DiscordReceiver(object):
    """
    receive message from telegram
    """

    def __init__(self):
        self.task = Task(queue=__receiver__)

    @staticmethod
    async def llm_request(llm_agent: OpenaiMiddleware, disable_function: bool = False):
        """
        校验包装，没有其他作用
        """
        try:
            _result = await llm_agent.request_openai(disable_function=disable_function)
            _message = _result.default_message
            logger.debug(f"[x] LLM Message Sent \n--message {_message}")
            assert _message, "message is empty"
            return _result
        except ssl.SSLSyscallError as e:
            logger.error(f"Network ssl error: {e},that maybe caused by bad proxy")
            raise e
        except RateLimitError as e:
            logger.error(f"ApiEndPoint:{e}")
            raise ValueError(f"Authentication expiration, overload or other issues with the Api Endpoint")
        except Exception as e:
            logger.exception(e)
            raise e

    async def _flash(self,
                     task: TaskHeader,
                     llm: OpenaiMiddleware,
                     auto_write_back: bool = True,
                     intercept_function: bool = False,
                     disable_function: bool = False
                     ):
        """
        函数池刷新
        :param auto_write_back: 是否将task携带的消息回写进消息池中，如果为False则丢弃task携带消息
        :param intercept_function: 是否拦截函数调用转发到函数处理器
        """
        try:
            llm.build(auto_write_back=auto_write_back)
            try:
                result = await self.llm_request(llm, disable_function=disable_function)
            except Exception as e:
                await __sender__.error(
                    receiver=task.receiver,
                    text=f"🦴 Sorry, your request failed because: {e}"
                )
                return
            if intercept_function:
                # 拦截函数调用
                if hasattr(result.default_message, "function_call"):
                    return await __sender__.function(
                        receiver=task.receiver,
                        task=task,
                        llm=llm,  # IMPORTANT
                        message=result.default_message,
                        result=result
                    )
            return await __sender__.reply(
                receiver=task.receiver,
                message=[result.default_message]
            )
        except Exception as e:
            raise e

    async def deal_message(self, message):
        """
        处理消息
        """
        # 解析数据
        _task: TaskHeader = TaskHeader.parse_raw(message.body)
        # 没有任何参数
        if _task.task_meta.direct_reply:
            await __sender__.forward(
                receiver=_task.receiver,
                message=_task.message
            )
            return None, None, None
            # 函数重整策略
        functions = None
        if _task.task_meta.function_enable:
            # 继承函数
            functions = _task.task_meta.function_list
            if _task.task_meta.sign_as[0] == 0:
                # 复制救赎
                _task.task_meta.function_salvation_list = _task.task_meta.function_list
                functions = []

                # 重整
                for _index, _message in enumerate(_task.message):
                    functions.extend(
                        ToolRegister().filter_pair(key_phrases=_message.text)
                    )
                _task.task_meta.function_list = functions
        if _task.task_meta.sign_as[0] == 0:
            # 容错一层旧节点
            functions.extend(_task.task_meta.function_salvation_list)
        # 构建通信代理
        _llm = OpenaiMiddleware(task=_task, function=functions)
        logger.debug(f"[x] Received Order \n--order {_task.json(indent=2)}")
        # 插件直接转发与重处理
        if _task.task_meta.callback_forward:
            # 手动追加插件产生的线索消息
            _llm.write_back(
                role=_task.task_meta.callback.role,
                name=_task.task_meta.callback.name,
                message_list=_task.message
            )
            # 插件数据响应到前端
            if _task.task_meta.callback_forward_reprocess:
                # 手动写回则禁用从 Task 数据体自动回写
                # 防止AI去启动其他函数，禁用函数
                await self._flash(
                    llm=_llm,
                    task=_task,
                    intercept_function=True,
                    disable_function=True,
                    auto_write_back=False
                )
                # 同时递交部署点
                return _task, _llm, "callback_forward_reprocess"
            # 转发函数
            await __sender__.forward(
                receiver=_task.receiver,
                message=_task.message
            )
            # 同时递交部署点
            return _task, _llm, "callback_forward_reprocess"
        await self._flash(llm=_llm, task=_task, intercept_function=True)
        return None, None, None

    async def on_message(self, message: AbstractIncomingMessage):
        # 过期时间
        # print(message.expiration)
        try:
            if os.getenv("LLMBOT_STOP_REPLY") == "1":
                return None
            _task, _llm, _point = await self.deal_message(message)
            # 启动链式函数应答循环
            if _task:
                chain: Chain = await ChainReloader(uid=_task.receiver.uid).get_task()
                if chain:
                    logger.info(f"Catch chain callback\n--callback_send_by {_point}")
                    await Task(queue=chain.address).send_task(task=chain.arg)
        except Exception as e:
            logger.exception(e)
            await message.reject(requeue=False)
        finally:
            await message.ack(multiple=False)

    async def discord(self):
        if not BotSetting.available:
            logger.warning("Receiver Runtime:Discord Setting empty")
            return None
        await discord_rest.start()
        __sender__.acquire()
        try:
            await self.task.consuming_task(self.on_message)
        except KeyboardInterrupt:
            logger.warning("Discord Receiver shutdown")
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            await discord_rest.close()


@atexit.register
def __clean():
    try:
        sync(discord_rest.close())
    except Exception as e:
        logger.warning(f"Discord Receiver cleaning failed when exiting \n{e}")
