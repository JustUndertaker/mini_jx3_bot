"""
通用数据结构，这里保存其他地方需要调用的数据模型。
"""
from nonebot.permission import Permission
from pydantic import BaseModel


class PluginConfig(BaseModel):
    '''插件使用的基本设置'''
    enable_managed: bool = True
    '''是否受插件管理器管理'''
    default_status: bool = True
    '''默认开关'''


async def _group_admin() -> bool:
    # TODO:待实现
    return False

GROUP_ADMIN = Permission(_group_admin)
"""匹配群管理员权限"""
