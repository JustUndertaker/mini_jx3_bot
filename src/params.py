"""
通用数据结构，这里保存其他地方需要调用的数据模型。
"""
from enum import Enum, auto

from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
# from nonebot.permission import Permission
from pydantic import BaseModel


class PluginConfig(BaseModel):
    '''插件使用的基本设置'''
    enable_managed: bool = True
    '''是否受插件管理器管理'''
    default_status: bool = True
    '''默认开关'''


# async def _group_admin() -> bool:
#    # TODO:待实现
#    return False
#
# GROUP_ADMIN=Permission(_group_admin)

GROUP_ADMIN = GROUP_ADMIN | GROUP_OWNER
"""匹配群管理员权限"""


class GroupSetting(Enum):
    '''
    群设置枚举
    '''
    进群通知 = auto()
    离群通知 = auto()
    晚安通知 = auto()
    开服推送 = auto()
    新闻推送 = auto()
    奇遇推送 = auto()
    抓马监控 = auto()
    扶摇监控 = auto()


class NoticeType(Enum):
    晚安通知 = auto()
    离群通知 = auto()
    进群通知 = auto()
