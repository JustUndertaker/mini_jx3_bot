from typing import Optional

from nonebot import export, on_message
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.params import Depends

from . import data_source as source

Export = export()
Export.plugin_name = "自动插话"
Export.plugin_command = "~"
Export.plugin_usage = "可以自动插话，频率与活跃度相关。"
Export.default_status = True

auto_chat = on_message(permission=GROUP, priority=99, block=True)


async def check(matcher: Matcher, event: GroupMessageEvent) -> Optional[str]:
    '''检测文字'''
    text = event.get_plaintext()
    if text == "":
        await matcher.finish()
    return text


@auto_chat.handle()
async def _(bot: Bot, event: GroupMessageEvent, text: str = Depends(check)):
    '''自动插话'''
    nickname = list(bot.config.nickname)[0]
    msg = await source.get_random_msg(event.group_id, nickname, text)
    await auto_chat.finish(msg)
