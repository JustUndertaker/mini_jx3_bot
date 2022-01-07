from typing import Optional

from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo


async def get_plugin_status(group_id: int, module_name: str) -> Optional[bool]:
    '''获取插件状态'''
    return await PluginInfo.get_plugin_status(group_id, module_name)


async def get_bot_status(group_id: int) -> Optional[bool]:
    '''获取机器人开启情况'''
    return await GroupInfo.get_bot_status(group_id)
