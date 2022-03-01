import random
from typing import Optional

from nonebot import export, on_message
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.rule import Rule

from . import data_source as source

Export = export()
Export.plugin_name = "自动插话"
Export.plugin_command = "~"
Export.plugin_usage = "可以自动插话，频率与活跃度相关。"
Export.default_status = True

# ----------------------------------------------------------------------------
#   rule检查，随机到后才会执行
# ----------------------------------------------------------------------------


async def _random_check(event: GroupMessageEvent) -> bool:
    group_id = event.group_id
    active = await source.get_active(group_id)
    random_num = random.uniform(0, 200)
    return random_num < active


def CheckRandom() -> bool:
    return Depends(_random_check)


class RandomRule:
    async def __call__(self, check: bool = CheckRandom()) -> bool:
        return check


def check_random() -> Rule:
    return Rule(RandomRule())


# ----------------------------------------------------------------------------
#   matcher实现
# ----------------------------------------------------------------------------


auto_chat = on_message(permission=GROUP, rule=check_random(), priority=99, block=True)


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
