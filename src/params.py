"""
通用数据结构，这里保存其他地方需要调用的数据模型。
"""
from enum import Enum, auto

from nonebot import MatcherGroup
from nonebot.adapters.onebot.v11 import (
    GROUP,
    GROUP_ADMIN,
    GROUP_OWNER,
    GroupMessageEvent,
    MessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.rule import Rule

# from nonebot.permission import Permission
from pydantic import BaseModel

from src.modules.user_info import UserInfo


class PluginConfig(BaseModel):
    """
    插件管理器需要的配置，如果没有此配置，插件管理器将不会管理
    """

    enable_managed: bool = True
    """
    是否受插件管理器管理，若设置成False，插件管理器将不会管理
    """
    default_status: bool = True
    """默认开关"""
    cost_gold: int = 0
    """
    使用花费，这里只是显示在菜单中，真正起效在params的cost_gold()
    """


def cost_gold(gold: int):
    """
    说明:
        Dependency，每次调用需要消耗金币数，用于插件使用金币

    参数:
        * `gold`：每次所需金币数

    用法:
    ```
        @matcher.handle(parameterless=[cost_gold(gold=0)])
        async def _():
            pass
    ```
    """

    async def dependency(matcher: Matcher, event: GroupMessageEvent):
        flag = await UserInfo.cost_gold(event.user_id, event.group_id, gold)
        if not flag:
            msg = MessageSegment.at(event.user_id) + "你的金币不够了，不能操作哟！"
            await matcher.finish(msg)

    return Depends(dependency)


class GroupSetting(Enum):
    """
    群设置枚举
    """

    进群通知 = auto()
    离群通知 = auto()
    晚安通知 = auto()
    开服推送 = auto()
    新闻推送 = auto()
    奇遇推送 = auto()
    抓马监控 = auto()
    扶摇监控 = auto()


class NoticeType(Enum):
    """
    群通知枚举
    """

    晚安通知 = auto()
    离群通知 = auto()
    进群通知 = auto()


def _check_event() -> Rule:
    """匹配私聊消息"""

    def check(event: MessageEvent) -> bool:
        return isinstance(event, PrivateMessageEvent)

    return Rule(check)


admin_matcher_group = MatcherGroup(
    rule=_check_event(), permission=SUPERUSER, priority=2, block=True
)
"""
说明:
    超级管理员命令组，超级管理员私聊触发，用于创建matcher
"""

group_matcher_group = MatcherGroup(
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=3, block=True
)
"""
说明:
    群管理命令组，群管和超级用户可以使用，用于创建matcher
"""

user_matcher_group = MatcherGroup(permission=GROUP, priority=5, block=True)
"""
说明：
    用户权限命令组，用于群组内普通用户创建matcher
"""
