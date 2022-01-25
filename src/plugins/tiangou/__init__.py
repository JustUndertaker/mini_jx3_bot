from nonebot import export, on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from src.utils.log import logger

from .data_source import get_tiangou

Export = export()
Export.plugin_name = "舔狗日记"
Export.plugin_command = "舔狗|日记|舔狗日记"
Export.plugin_usage = "发送一条舔狗日记"
Export.default_status = True


tiangou_regex = r"(^舔狗$)|(^日记$)|(^舔狗日记$)"
tiangou = on_regex(pattern=tiangou_regex, permission=GROUP, priority=5, block=True)


@tiangou.handle()
async def _(event: GroupMessageEvent):
    '''舔狗日记'''
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 舔狗日记 | 请求日记"
    )
    msg = await get_tiangou()
    await tiangou.finish(msg)
