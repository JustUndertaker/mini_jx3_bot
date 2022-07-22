from datetime import date

from nonebot.adapters.onebot.v11.message import MessageSegment

from src.utils.browser import browser

from .model import coro_api


async def get_data(name: str) -> MessageSegment:
    """
    说明:
        根据城市名称，获取新冠疫情信息

    参数:
        `name`：输入城市名称

    返回:
        `MessageSegment`：机器人回复消息
    """
    city_info = coro_api.get_city(name)
    if not city_info.legal:
        return MessageSegment.text("查询失败，请检查参数！")
    response = await coro_api.get_coro_data(city_info)
    if not response:
        return MessageSegment.text("查询失败，浏览器出错嘞!")

    data = response.dict()

    time_now = date.today()
    data["time"] = time_now.strftime("%Y-%m-%d")
    pagename = "疫情查询.html"
    img = await browser.template_to_image(pagename=pagename, data=data)
    return MessageSegment.image(img)
