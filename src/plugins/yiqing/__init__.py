from nonebot import on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.params import PluginConfig, cost_gold
from src.utils.log import logger

from .data_source import get_data

__plugin_meta__ = PluginMetadata(
    name="疫情查询",
    description="查询疫情情况。",
    usage="XX疫情 | 疫情 XX",
    config=PluginConfig(cost_gold=10),
)

yiqing = on_regex(
    r"(?P<value1>[\u4e00-\u9fa5]+)疫情$|^疫情 (?P<value2>[\u4e00-\u9fa5]+)$",
    permission=GROUP,
    priority=5,
    block=True,
)


def get_name(regex_dict: dict = RegexDict()) -> str:
    """
    说明:
        Dependency，获取匹配字符串中的value字段
    """
    value = regex_dict.get("value1")
    return value if value else regex_dict.get("value2")


@yiqing.handle(parameterless=[cost_gold(gold=10)])
async def _(event: GroupMessageEvent, name: str = Depends(get_name)):
    """疫情查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 疫情查询 | 请求：{name}")
    msg = await get_data(name)
    await yiqing.finish(msg)
