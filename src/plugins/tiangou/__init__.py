from nonebot import on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.plugin import PluginMetadata
from src.params import PluginConfig, cost_gold
from src.utils.log import logger

from .data_source import get_tiangou

__plugin_meta__ = PluginMetadata(
    name="舔狗日记",
    description="发送一条舔狗日记。",
    usage="舔狗 | 日记 | 舔狗日记",
    config=PluginConfig(cost_gold=10)
)


tiangou_regex = r"(^舔狗$)|(^日记$)|(^舔狗日记$)"
tiangou = on_regex(pattern=tiangou_regex, permission=GROUP, priority=5, block=True)


@tiangou.handle(parameterless=[cost_gold(gold=10)])
async def _(event: GroupMessageEvent):
    '''舔狗日记'''
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 舔狗日记 | 请求日记"
    )
    msg = await get_tiangou()
    await tiangou.finish(msg)
