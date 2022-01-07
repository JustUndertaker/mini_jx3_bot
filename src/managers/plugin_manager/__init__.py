from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor

from . import data_source as source


@run_postprocessor
async def _(matcher: Matcher, event: GroupMessageEvent):
    '''插件管理系统，事件预处理'''
    # 检测插件是否注册
    group_id = event.group_id
    module_name = matcher.plugin_name
    status = await source.get_plugin_status(group_id, module_name)
    if status is None:
        # 跳过未注册的插件
        return

    if not status:
        # 停止未开启的插件
        raise IgnoredException("插件未开启")

    # 检测机器人总开关
    bot_status = await source.get_bot_status(group_id)
    if not bot_status:
        raise IgnoredException("机器人未开启")
