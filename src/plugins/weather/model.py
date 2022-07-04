from datetime import datetime
from typing import Literal, Optional

from httpx import AsyncClient
from pydantic import BaseModel

from src.utils.config import weather_config
from src.utils.log import logger


class Now(BaseModel):
    """实时天气数据"""

    obsTime: str
    """数据观测时间"""
    temp: str
    """温度，默认单位：摄氏度"""
    feelsLike: str
    """体感温度，默认单位：摄氏度"""
    icon: str
    """天气状况和图标的代码"""
    text: str
    """天气状况的文字描述"""
    wind360: str
    """风向360角度"""
    windDir: str
    """风向"""
    windScale: str
    """风力等级"""
    windSpeed: str
    """风速，公里/小时"""
    humidity: str
    """相对湿度，百分比数值"""
    precip: str
    """当前小时累计降水量，默认单位：毫米"""
    pressure: str
    """大气压强，默认单位：百帕"""
    vis: str
    """能见度，默认单位：公里"""
    cloud: Optional[str]
    """云量，百分比数值。可能为空"""
    dew: Optional[str]
    """露点温度。可能为空"""


class NowApiResponse(BaseModel):
    """实时天气接口返回"""

    code: str
    """API状态码"""
    updateTime: str
    """当前API的最近更新时间"""
    now: Now
    """实时数据"""


class Daily(BaseModel):
    """逐天天气数据"""

    fxDate: str
    """预报日期"""
    week: Optional[str]
    date: Optional[str]
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyApi(BaseModel):
    code: str
    daily: list[Daily]


class Air(BaseModel):
    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: Optional[str]


class AirApi(BaseModel):
    code: str
    now: Optional[Air]


class Warning(BaseModel):
    title: str
    type: str
    pubTime: str
    text: str


class WarningApi(BaseModel):
    code: str
    warning: list[Warning]


class Weather:
    """请求天气封装"""

    api_key: str
    """和风天气的apikey"""
    days_type: Literal["3d", "7d"]
    """最多请求天数，普通版只能3天"""
    weather_api_url: str
    """请求天气api地址"""
    geo_api_url: str
    """请求城市id地址"""
    weather_warning_url: str
    """天气灾害预警地址"""
    client: AsyncClient
    """httpx异步客户端"""

    def __init__(self):
        self.api_key = weather_config.api_key
        api_type = weather_config.api_type
        match api_type:
            case 0:
                # 普通版apikey
                self.weather_api_url = "https://devapi.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/"
                self.weather_warning_url = "https://devapi.qweather.com/v7/warning/now"
                self.days_type = "3d"
            case 1:
                # 个人开发版apikey
                self.weather_api_url = "https://devapi.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/"
                self.weather_warning_url = "https://devapi.qweather.com/v7/warning/now"
                self.days_type = "7d"
            case 2:
                # 商业版apikey
                self.weather_api_url = "https://api.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/"
                self.weather_warning_url = "https://api.qweather.com/v7/warning/now"
                self.days_type = "7d"
        self.client = AsyncClient()

    @classmethod
    def _handle_days(cls, days: list[dict[str, str]]) -> dict:
        """处理days数据，增加week，date字段"""
        week_map = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        data = []
        today = True
        for one_day in days:
            _date = one_day["fxDate"].split("-")
            _year = int(_date[0])
            _month = int(_date[1])
            _day = int(_date[2])
            week = int(datetime(_year, _month, _day).strftime("%w"))
            one_day["week"] = "今日" if today else week_map[week]
            today = False
            one_day["date"] = f"{_month}月{_day}日"
            data.append(one_day)
        return data

    async def _get_city_info(
        self, city_kw: str, api_type: str = "lookup"
    ) -> tuple[Optional[int], Optional[str]]:
        """
        :说明
            获取城市信息

        :参数
            * city_kw：请求名称
            * api_type：请求方法，默认为“lookup”

        :返回
            * city_id：城市id
            * city_name：城市名
        """
        url = self._geoapi + api_type
        params = {"location": city_kw, "key": self._api_key}
        try:
            req = await self._client.get(url=url, params=params)
            req_json: dict = req.json()
            code = req_json["code"]
            city_id: int = int(req_json["location"][0]["id"])
            city_name: str = req_json["location"][0]["name"]
            if code != "200":
                log = f"<r>获取城市id失败，code：{code}</r>"
                logger.error(log)
                return None, None
            return city_id, city_name

        except Exception as e:
            log = f"<r>获取城市id接口失败：{str(e)}</r>"
            logger.error(log)
            return None, None

    async def _get_weather_info(self, api_type: str, city_id: int) -> Optional[dict]:
        """
        :说明
            获取城市天气信息

        :参数
            * api_type：请求方式
            * city_id：城市id

        :返回
            * dict：返回数据
        """
        url = self._weather_api + api_type
        params = {"location": city_id, "key": self._api_key}
        try:
            req = await self._client.get(url=url, params=params)
            req_json: dict = req.json()
            code = req_json["code"]
            if code != "200":
                log = f"<r>获取天气消息失败，code：{code}</r>"
                logger.error(log)
                return None
            return req_json
        except Exception as e:
            log = f"<r>访问天气接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def _get_weather_warning(self, city_id: str) -> Optional[dict]:
        """
        :说明
            获取城市天气预警信息

        :参数
            * city_id：城市id

        :返回
            * dict：返回数据
        """
        params = {"location": city_id, "key": self._api_key}
        try:
            req = await self._client.get(url=self._weather_warning, params=params)
            req_json: dict = req.json()
            code = req_json["code"]
            if code != "200":
                log = f"<r>获取天气预警失败，code：{code}</r>"
                logger.error(log)
                return None
            return req_json

        except Exception as e:
            log = f"<r>访问天气预警接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def get_weather(self, city: str) -> Optional[dict]:
        """
        :说明
            获取城市天气

        :参数
            * city：城市名

        :返回
            * dict：天气数据字典
        """
        city_id, city_name = await self._get_city_info(city)
        if not city_id:
            return None
        daily_info = await self._get_weather_info(self._days_type, city_id)
        now_info = await self._get_weather_info("now", city_id)
        if not daily_info or not now_info:
            return None
        warning = await self._get_weather_warning(city_id)
        if not warning:
            return None
        days: list = daily_info["daily"]
        days = self._handle_days(days)
        now = now_info["now"]
        data = {"city": city_name, "now": now, "days": days, "warning": warning}
        return data


weather_client = Weather()
"""天气请求客户端"""
