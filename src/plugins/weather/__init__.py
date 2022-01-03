from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP

from .data_source import get_weather

weather_regex = r"([\u4e00-\u9fa5]+天气$)|(^天气 [\u4e00-\u9fa5]+$)"
weather = on_regex(pattern=weather_regex, permission=GROUP, priority=5, block=True)


@weather.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''查询天气'''
    get_msg = event.get_plaintext()
    msg_list = get_msg.split(" ")
    if len(msg_list) > 1:
        city = msg_list[-1]
    else:
        city = get_msg[:-2]
    msg = await get_weather(city)
    await weather.finish(msg)
