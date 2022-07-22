from nonebot import on_message
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from src.internal.nlp import chat
from src.params import PluginConfig
from src.utils.log import logger

__plugin_meta__ = PluginMetadata(
    name="智能闲聊",
    description="闲聊功能，有一句没一句",
    usage="@机器人 +你要说的话",
    config=PluginConfig(),
)


chat_query = on_message(rule=to_me(), permission=GROUP, priority=9, block=True)


@chat_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """智能闲聊"""
    nickname = list(bot.config.nickname)[0]
    message = event.get_plaintext()
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求：{message}")
    msg = await chat.chat(nickname, message)
    await chat_query.finish(msg)
