from typing import Optional, Union

from httpx import AsyncClient
from pydantic import BaseModel

from src.utils.log import logger

from .config import CITY_MAP


class Response(BaseModel):
    """返回数据模型"""

    cityName: str
    """城市名称"""
    currentConfirmedCount: Union[int, str]
    """现存确诊"""
    confirmedCount: Union[int, str]
    """累计确诊"""
    suspectedCount: Union[int, str]
    """疑似病例"""
    curedCount: Union[int, str]
    """累计治愈"""
    deadCount: Union[int, str]
    """累计死亡"""
    highDangerCount: Union[int, str]
    """重症病例"""


class CityInfo(BaseModel):
    """城市信息"""

    legal: bool
    """参数是否合法"""
    province: Optional[str]
    """省份"""
    city: Optional[str]
    """城市"""


class CoroData:
    """新冠查询接口封装"""

    client: AsyncClient
    """查询客户端"""
    url: str
    """查询地址"""

    def __init__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Charset": "utf-8",
        }
        self.client = AsyncClient(headers=headers)
        self.url = "https://api.yimian.xyz/coro/"

    def get_city(self, name: str) -> CityInfo:
        """
        说明:
            根据输入的城市名称，获取城市信息

        参数:
            `name`：输入城市名称

        返回:
            `CityInfo`：城市信息
        """
        if name in CITY_MAP:
            if CITY_MAP[name] == "":
                return CityInfo(legal=True, province=name, city="")
            else:
                return CityInfo(legal=True, province=CITY_MAP[name], city=name)
        else:
            return CityInfo(legal=False)

    async def get_coro_data(self, city: CityInfo) -> Optional[Response]:
        """
        说明:
            根据城市信息，获取新冠疫情数据

        参数:
            `city`：城市信息

        返回:
            `Response`：新冠疫情数据
        """
        params = {"province": city.province, "city": city.city}
        try:
            resp = await self.client.get(url=self.url, params=params)
            data = resp.json()
            res_data = Response.parse_obj(data)
            if res_data.cityName == "":
                res_data.cityName = city.city
            if res_data.currentConfirmedCount == 0:
                res_data.currentConfirmedCount = "-"
            if res_data.confirmedCount == 0:
                res_data.confirmedCount = "-"
            if res_data.suspectedCount == 0:
                res_data.suspectedCount = "-"
            if res_data.curedCount == 0:
                res_data.curedCount = "-"
            if res_data.deadCount == 0:
                res_data.deadCount = "-"
            if res_data.highDangerCount == 0:
                res_data.highDangerCount = "-"
            return res_data
        except Exception as e:
            logger.error(f"<y>疫情查询</y> | 查询失败：{str(e)}")
            return None


coro_api = CoroData()
"""新冠疫情查询接口"""
