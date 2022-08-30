from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.internal.plugin_manager import plugin_manager
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.params import GroupSetting, PluginConfig, group_matcher_group
from src.utils.log import logger

__plugin_meta__ = PluginMetadata(
    name="插件管理插件",
    description="用来控制插件的开关",
    usage="群管理输入[打开 | 关闭] 插件名称",
    config=PluginConfig(enable_managed=False),
)


@run_preprocessor
async def _(matcher: Matcher, event: GroupMessageEvent):
    """
    插件管理，基于hook实现插件开关
    """
    # 检测插件是否注册
    group_id = event.group_id
    module_name = matcher.plugin_name
    status = await PluginInfo.get_plugin_status(group_id, module_name)
    if status is None:
        # 跳过未注册的插件
        return

    if not status:
        # 停止未开启的插件
        raise IgnoredException("插件未开启")

    # 检测机器人总开关
    bot_status = await GroupInfo.get_bot_status(group_id)
    if not bot_status:
        raise IgnoredException("机器人未开启")


# -----------------------------------------------------------------------------
# Depends: 依赖注入函数
# -----------------------------------------------------------------------------
def get_group_setting() -> GroupSetting:
    """
    说明:
        Dependency，获取群设置类型
    """

    def dependency(matcher: Matcher, regex_dict: dict = RegexDict()) -> GroupSetting:
        match regex_dict["value"]:
            case "进群通知":
                return GroupSetting.进群通知
            case "离群通知":
                return GroupSetting.离群通知
            case "晚安通知":
                return GroupSetting.晚安通知
            case "开服推送":
                return GroupSetting.开服推送
            case "新闻推送":
                return GroupSetting.新闻推送
            case "奇遇推送":
                return GroupSetting.奇遇推送
            case "抓马监控":
                return GroupSetting.抓马监控
            case "扶摇监控":
                return GroupSetting.扶摇监控
            case _:
                matcher.skip()

    return Depends(dependency)


def get_plugin_name() -> str:
    """
    说明:
        Dependency，获取插件模块名称
    """

    async def dependency(matcher: Matcher, regex_dict: dict = RegexDict()) -> str:
        plugin_name = regex_dict["value"]
        module_name = plugin_manager.get_module_name(plugin_name)
        if not module_name:
            await matcher.finish(f"未找到插件[{plugin_name}]。")
        return module_name

    return Depends(dependency)


def get_status() -> bool:
    """
    说明:
        Dependency，获取开关状态
    """

    def dependency(regex_dict: dict = RegexDict()) -> bool:
        return regex_dict["status"] == "打开"

    return Depends(dependency)


# ----------------------------------------------------------------------------
#   插件开关指令管理，开关有2层：
#   第一层：群ws接收消息开关和各类设置开关
#   第二层：plugins插件开关
#   2层通用一个“打开|关闭 [name]”指令，所以要做2次判断，目前通过优先级来传递
# -----------------------------------------------------------------------------
regex = r"^(?P<status>打开|关闭) (?P<value>[\u4e00-\u9fa5]+)$"
# 群设置
group_status = group_matcher_group.on_regex(pattern=regex, block=False)
# 插件设置
plugin_status = group_matcher_group.on_regex(pattern=regex)


@group_status.handle()
async def _(
    event: GroupMessageEvent,
    config_type: GroupSetting = get_group_setting(),
    status: bool = get_status(),
):
    """群设置开关"""
    logger.info(
        f"<y>插件管理</y> | <g>群{event.group_id}</g> | 设置通知 | {config_type.name} | {'打开' if status else '关闭'}"
    )
    flag = await GroupInfo.set_config_status(event.group_id, config_type, status)
    msg = None
    if flag:
        group_status.stop_propagation(group_status)
        msg = f"设置成功！\n[{config_type.name}]当前已 {'打开' if status else '关闭'}"
    await group_status.finish(msg)


@plugin_status.handle()
async def _(
    event: GroupMessageEvent,
    module_name: str = get_plugin_name(),
    status: bool = get_status(),
    regex_dict: dict = RegexDict(),
):
    """设置插件开关"""
    plugin_name = regex_dict["value"]
    logger.info(
        f"<y>插件管理</y> | <g>群{event.group_id}</g> | 插件开关 | {plugin_name} | {'打开' if status else '关闭'}"
    )

    flag = await PluginInfo.set_plugin_status(event.group_id, module_name, status)
    if flag:
        msg = f"设置成功！\n插件[{plugin_name}]当前已 {'打开' if status else '关闭'}"
    else:
        msg = f"设置失败！未找到插件[{plugin_name}]"
    await plugin_status.finish(msg)
