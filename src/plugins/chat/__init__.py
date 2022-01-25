from nonebot import export, on_message
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.rule import to_me
from src.utils.log import logger

from .model import chat

Export = export()
Export.plugin_name = "智能闲聊"
Export.plugin_command = "@机器人 +你要说的话"
Export.plugin_usage = "闲聊功能，有一句没一句"
Export.default_status = True


chat_query = on_message(rule=to_me(), permission=GROUP, priority=9, block=True)


@chat_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''智能闲聊'''
    nickname = list(bot.config.nickname)[0]
    message = event.get_plaintext()
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 智能闲聊 | 请求：{message}"
    )
    msg = await chat.chat(nickname, message)
    await chat_query.finish(msg)
