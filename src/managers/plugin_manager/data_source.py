from typing import Literal, Optional

from nonebot.plugin import get_loaded_plugins
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo


async def get_plugin_status(group_id: int, module_name: str) -> Optional[bool]:
    '''获取插件状态'''
    return await PluginInfo.get_plugin_status(group_id, module_name)


async def get_bot_status(group_id: int) -> Optional[bool]:
    '''获取机器人开启情况'''
    return await GroupInfo.get_bot_status(group_id)


def _chinese_to_bool(string: Literal["打开", "关闭"]) -> bool:
    '''将开关解析为bool'''
    return (string == "打开")


async def change_group_config(group_id: int, config_type: str, status: Literal["打开", "关闭"]) -> bool:
    '''
    :说明
        改变群设置

    :参数
        * group_id：QQ群号
        * config_type：开关类型
        * status：开关

    :返回
        * bool：如果有设置，则成功，没有改设置会返回False
    '''

    _config_type = None
    if config_type == "进群通知":
        _config_type = "welcome_status"
    if config_type == "离群通知":
        _config_type = "someoneleft_status"
    if config_type == "晚安通知":
        _config_type = "goodnight_status"
    if config_type == "开服推送":
        _config_type = "ws_server"
    if config_type == "新闻推送":
        _config_type = "ws_news"
    if config_type == "奇遇推送":
        _config_type = "ws_serendipity"
    if config_type == "抓马监控":
        _config_type = "ws_horse"
    if config_type == "扶摇监控":
        _config_type = "ws_fuyao"
    if _config_type:
        _status = _chinese_to_bool(status)
        await GroupInfo.set_config_status(group_id, _config_type, _status)
        return True
    return False


async def change_plugin_status(group_id: int, plugin_name: str, status: Literal["打开", "关闭"]) -> bool:
    '''
    :说明
        改变插件开关

    :参数
        * group_id：QQ群号
        * plugin_name：插件名称
        * status：开关

    :返回
        * bool：如果有设置，则成功，没有改设置会返回False
    '''
    flag = False
    module_name = ""
    plugins = list(get_loaded_plugins())
    for one_plugin in plugins:
        export = one_plugin.export
        _plugin_name = export.get("plugin_name")
        if _plugin_name == plugin_name:
            flag = True
            module_name = one_plugin.name
    if flag:
        _status = _chinese_to_bool(status)
        return await PluginInfo.set_plugin_status(group_id, module_name, _status)
    return False
