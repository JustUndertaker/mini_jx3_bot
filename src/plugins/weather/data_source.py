from nonebot.adapters.onebot.v11 import MessageSegment
from src.utils.browser import browser
from src.utils.log import logger

from ._weather import weather_client


async def get_weather(city: str) -> MessageSegment:
    '''
    :说明
        获取天气图片

    :参数
        * city：城市名

    :返回
        * MessageSegment：输出消息
    '''
    data = await weather_client.get_weather(city)
    if not data:
        logger.debug(
            "<y>天气查询</y> | 请求数据失败！"
        )
        return MessageSegment.text("天气数据请求失败了！")
    logger.debug(
        f"<y>天气查询</y> | 返回：{data}"
    )
    pagename = "weather.html"
    image = await browser.template_to_image(pagename=pagename,
                                            now=data['now'],
                                            days=data['days'],
                                            city=data['city'],
                                            warning=data['warning']
                                            )
    return MessageSegment.image(image)
