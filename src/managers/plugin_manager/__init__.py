from nonebot import on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.permission import SUPERUSER
from src.utils.log import logger

from . import data_source as source


@run_preprocessor
async def _(matcher: Matcher, event: GroupMessageEvent):
    '''插件管理系统，插件开关实现'''
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


# ----------------------------------------------------------------------------
#   插件开关指令管理，开关有2层：
#   第一层：群ws接收消息开关和各类设置开关
#   第二层：plugins插件开关
#   2层通用一个“打开|关闭 [name]”指令，所以要做2次判断，目前通过优先级来传递
# -----------------------------------------------------------------------------
regex = r"^(打开|关闭) [\u4e00-\u9fa5]+$"
group_status = on_regex(pattern=regex,
                        permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                        priority=2, block=False)  # 群设置

plugin_status = on_regex(pattern=regex,
                         permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                         priority=3, block=True)  # 插件设置


@group_status.handle()
async def _(matcher: Matcher, event: GroupMessageEvent):
    '''群设置开关'''
    get_msg = event.get_plaintext().split(" ")
    status = get_msg[0]
    config_type = get_msg[-1]
    logger.info(
        f"<y>插件管理</y> | <g>群{event.group_id}</g> | 设置通知 | {config_type} | {status}"
    )
    flag = await source.change_group_config(event.group_id, config_type, status)
    if flag:
        matcher.stop_propagation()
        await group_status.finish(
            f"设置成功！\n[{config_type}]当前已 {status}"
        )
    await group_status.finish()


@plugin_status.handle()
async def _(event: GroupMessageEvent):
    '''设置插件开关'''
    get_msg = event.get_plaintext().split(" ")
    status = get_msg[0]
    plugin_name = get_msg[-1]
    logger.info(
        f"<y>插件管理</y> | <g>群{event.group_id}</g> | 插件开关 | {plugin_name} | {status}"
    )
    flag = await source.change_plugin_status(event.group_id, plugin_name, status)
    if flag:
        msg = f"设置成功！\n插件[{plugin_name}]当前已 {status}"
    else:
        msg = f"设置失败！未找到插件[{plugin_name}]"
    await plugin_status.finish(msg)
