import random

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule

from src.modules.group_info import GroupInfo
from src.params import PluginConfig

from .data_source import get_random_msg

__plugin_meta__ = PluginMetadata(
    name="自动插话",
    description="可以自动插话，频率与活跃度相关。",
    usage="~",
    config=PluginConfig(default_status=False),
)

# ----------------------------------------------------------------------------
#   rule检查，随机到后才会执行
# ----------------------------------------------------------------------------


def check_random() -> Rule:
    async def _random_check(event: GroupMessageEvent) -> bool:
        group_id = event.group_id
        active = await GroupInfo.get_bot_active(group_id)
        random_num = random.uniform(0, 200)
        return random_num < active

    return Rule(_random_check)


# ----------------------------------------------------------------------------
#   matcher实现
# ----------------------------------------------------------------------------


auto_chat = on_message(permission=GROUP, rule=check_random(), priority=99, block=True)


async def check(matcher: Matcher, event: GroupMessageEvent) -> str:
    """检测文字"""
    text = event.get_plaintext()
    if text == "":
        await matcher.finish()
    return text


@auto_chat.handle()
async def _(bot: Bot, event: GroupMessageEvent, text: str = Depends(check)):
    """自动插话"""
    nickname = list(bot.config.nickname)[0]
    msg = await get_random_msg(event.group_id, nickname, text)
    await auto_chat.finish(msg)
