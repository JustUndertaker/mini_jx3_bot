from nonebot import export, on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import Depends
from src.utils.log import logger

from . import data_source as source

Export = export()
Export.plugin_name = "疫情查询"
Export.plugin_command = "XX疫情 | 疫情 XX"
Export.plugin_usage = "查询疫情状况。"
Export.default_status = True

yiqing = on_regex(r"([\u4e00-\u9fa5]+疫情$)|(^疫情 [\u4e00-\u9fa5]+$)", permission=GROUP,  priority=5, block=True)


def get_name(event: GroupMessageEvent) -> str:
    '''获取name'''
    text = event.get_plaintext()
    text_list = text.split(" ")
    if len(text_list) == 1:
        return text[:-2]
    else:
        return text_list[-1]


@yiqing.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_name)):
    '''疫情查询'''
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 疫情查询 | 请求：{name}"
    )
    msg = await source.get_data(name)
    await yiqing.finish(msg)
