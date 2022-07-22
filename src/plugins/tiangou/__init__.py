from datetime import datetime

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent
from nonebot.plugin import PluginMetadata

from src.internal.jx3api import JX3API
from src.params import PluginConfig, cost_gold
from src.utils.log import logger

__plugin_meta__ = PluginMetadata(
    name="舔狗日记",
    description="发送一条舔狗日记。",
    usage="舔狗 | 日记 | 舔狗日记",
    config=PluginConfig(cost_gold=1),
)

api = JX3API()


tiangou_regex = r"(^舔狗$)|(^日记$)|(^舔狗日记$)"
tiangou = on_regex(pattern=tiangou_regex, permission=GROUP, priority=5, block=True)


@tiangou.handle(parameterless=[cost_gold(gold=1)])
async def _(event: GroupMessageEvent):
    """舔狗日记"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 请求日记")
    response = await api.transmit_random()
    msg = None
    if response.code == 200:
        text = response.data["text"]
        date_now = datetime.now()
        date_str = date_now.strftime("%Y年%m月%d日")
        msg = date_str + "\n" + text
    await tiangou.finish(msg)
