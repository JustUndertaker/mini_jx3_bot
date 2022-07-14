import asyncio
from datetime import date
from typing import Literal, Optional

from httpx import AsyncClient
from pydantic import BaseModel

from src.config import weather_config
from src.utils.log import logger


class CityInfo(BaseModel):
    """城市信息数据"""

    name: str
    """城市名"""
    id: str
    """城市id"""


class CityApiResponse(BaseModel):
    """城市信息返回"""

    code: str
    """返回码"""
    location: Optional[list[CityInfo]]
    """城市信息"""


class Now(BaseModel):
    """实时天气数据"""

    obsTime: str
    """数据观测时间"""
    temp: str
    """温度，默认单位：摄氏度"""
    icon: str
    """天气状况和图标的代码"""
    text: str
    """天气状况的文字描述"""
    windDir: str
    """风向"""
    windScale: str
    """风力等级"""
    humidity: str
    """相对湿度，百分比数值"""
    precip: str
    """当前小时累计降水量，默认单位：毫米"""
    vis: str
    """能见度，默认单位：公里"""


class NowApiResponse(BaseModel):
    """实时天气接口返回"""

    code: str
    """API状态码"""
    updateTime: Optional[str]
    """当前API的最近更新时间"""
    now: Optional[Now]
    """实时数据"""


class Daily(BaseModel):
    """逐天天气数据"""

    fxDate: str
    """预报日期"""
    week: Optional[str]
    """星期"""
    date: Optional[str]
    """日期"""
    tempMax: str
    """预报当天最高温度"""
    tempMin: str
    """预报当天最低温度"""
    textDay: str
    """预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述"""
    textNight: str
    """预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述"""
    iconDay: str
    """预报白天天气状况的图标代码"""
    iconNight: str
    """预报夜间天气状况的图标代码"""


class DailyApiResponse(BaseModel):
    """逐天天气接口返回"""

    code: str
    """API状态码"""
    daily: Optional[list[Daily]]
    """逐天天气数据"""


class Air(BaseModel):
    """空气质量数据"""

    category: str
    """空气质量指数级别"""
    aqi: str
    """空气质量指数"""
    pm2p5: str
    """PM2.5"""
    pm10: str
    """	PM10"""
    o3: str
    """臭氧"""
    co: str
    """一氧化碳"""
    no2: str
    """二氧化氮"""
    so2: str
    """二氧化硫"""
    tag_color: Optional[str]
    """tag颜色"""


class AirApiResponse(BaseModel):
    """空气质量接口返回"""

    code: str
    """API状态码"""
    now: Optional[Air]
    """当前空气质量数据"""


class Warning(BaseModel):
    """预警信息"""

    title: str
    """预警信息标题"""
    type: str
    """预警类型ID"""
    pubTime: str
    """预警发布时间"""
    text: str
    """预警详细文字描述"""


class WarningApiResponse(BaseModel):
    """预警信息接口返回"""

    code: str
    """API状态码"""
    warning: Optional[list[Warning]]
    """预警信息"""


class Weather:
    """请求天气封装"""

    api_key: str
    """和风天气的apikey"""
    days_type: Literal["3d", "7d"]
    """最多请求天数，普通版只能3天"""
    weather_api_url: str
    """天气查询url"""
    geo_api_url: str
    """城市信息查询url"""
    weather_warning_url: str
    """天气灾害预警url"""
    air_url: str
    """空气质量url"""
    client: AsyncClient
    """httpx异步客户端"""

    def __init__(self):
        self.api_key = weather_config.api_key
        api_type = weather_config.api_type
        match api_type:
            case 0:
                # 普通版apikey
                self.weather_api_url = "https://devapi.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/lookup"
                self.weather_warning_url = "https://devapi.qweather.com/v7/warning/now"
                self.air_url = "https://devapi.qweather.com/v7/air/now"
                self.days_type = "3d"
            case 1:
                # 个人开发版apikey
                self.weather_api_url = "https://devapi.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/lookup"
                self.weather_warning_url = "https://devapi.qweather.com/v7/warning/now"
                self.days_type = "7d"
                self.air_url = "https://devapi.qweather.com/v7/air/now"
            case 2:
                # 商业版apikey
                self.weather_api_url = "https://api.qweather.com/v7/weather/"
                self.geo_api_url = "https://geoapi.qweather.com/v2/city/lookup"
                self.weather_warning_url = "https://api.qweather.com/v7/warning/now"
                self.air_url = "https://api.qweather.com/v7/air/now"
                self.days_type = "7d"
        self.client = AsyncClient()

    @classmethod
    def handle_days(cls, daily: list[Daily]) -> list[Daily]:
        """
        说明:
            处理days数据，增加week，date字段

        参数:
            * `daily`：日常数据列表

        返回:
            * `list[Daily]`：处理后数据
        """
        week_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        today = True
        for one_day in daily:
            _date = date.fromisoformat(one_day.fxDate)
            one_day.week = "今日" if today else week_map[_date.weekday()]
            today = False
            one_day.date = f"{_date.month}月{_date.day}日"
        return daily

    async def _get_city(self, city: str) -> Optional[CityInfo]:
        """
        说明:
            获取城市信息

        参数:
            * `city`：请求城市名称

        :返回
            * `CityInfo`：城市信息
        """
        params = {"location": city, "key": self.api_key}
        try:
            req = await self.client.get(url=self.geo_api_url, params=params)
            response = CityApiResponse.parse_obj(req.json())
            if response.code != "200":
                logger.error(f"<r>获取城市id失败，code：{response.code}</r>")
                return None
            return response.location[0]

        except Exception as e:
            log = f"<r>获取城市id接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def _get_weather_now(self, city_id: str) -> Optional[Now]:
        """
        说明:
            获取实时天气信息

        参数:
            * `city_id`：城市id

        返回:
            * `Now`：天气信息
        """
        url = self.weather_api_url + "now"
        params = {"location": city_id, "key": self.api_key}
        try:
            req = await self.client.get(url=url, params=params)
            response = NowApiResponse.parse_obj(req.json())
            if response.code != "200":
                log = f"<r>获取实时天气失败，code：{response.code}</r>"
                logger.error(log)
                return None
            return response.now
        except Exception as e:
            log = f"<r>访问天气接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def _get_weather_daily(self, city_id: str) -> Optional[list[Daily]]:
        """
        说明:
            获取逐天天气信息

        参数:
            * `city_id`：城市id

        返回:
            * `list[Daily]`：逐天天气信息
        """
        url = self.weather_api_url + self.days_type
        params = {"location": city_id, "key": self.api_key}
        try:
            req = await self.client.get(url=url, params=params)
            response = DailyApiResponse.parse_obj(req.json())
            if response.code != "200":
                log = f"<r>获取逐天天气失败，code：{response.code}</r>"
                logger.error(log)
                return None
            return self.handle_days(response.daily)
        except Exception as e:
            log = f"<r>访问天气接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def _get_weather_warning(self, city_id: str) -> Optional[list[Warning]]:
        """
        说明:
            获取天气预警信息

        参数:
            * `city_id`：城市id

        返回:
            * `list[Warning]`：返回数据
        """
        params = {"location": city_id, "key": self.api_key}
        try:
            req = await self.client.get(url=self.weather_warning_url, params=params)
            response = WarningApiResponse.parse_obj(req.json())
            if response.code != "200":
                log = f"<r>获取天气预警失败，code：{response.code}</r>"
                logger.error(log)
                return None
            return response.warning

        except Exception as e:
            log = f"<r>访问天气预警接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def _get_air_info(self, city_id: str) -> Optional[Air]:
        """
        说明:
            获取空气质量信息

        参数:
            * `city_id`：城市id

        返回:
            * `Air`：空气质量信息
        """
        params = {"location": city_id, "key": self.api_key}
        try:
            req = await self.client.get(url=self.air_url, params=params)
            response = AirApiResponse.parse_obj(req.json())
            if response.code != "200":
                log = f"<r>获取空气质量失败，code：{response.code}</r>"
                logger.error(log)
                return None
            return response.now
        except Exception as e:
            log = f"<r>访问空气质量接口失败：{str(e)}</r>"
            logger.error(log)
            return None

    async def get_weather(self, city: str) -> Optional[dict]:
        """
        说明:
            获取城市天气信息

        参数:
            * `city`：城市名

        返回:
            * `dict`：天气数据字典
                * `city`：城市名
                * `now`：实时天气信息
                * `daily`：逐天天气信息
                * `warning`：天气预警信息
                * `air`：空气质量信息
        """
        res_city = await self._get_city(city)
        if not res_city:
            return None
        res_now, res_daily, res_warning, res_air = await asyncio.gather(
            self._get_weather_now(res_city.id),
            self._get_weather_daily(res_city.id),
            self._get_weather_warning(res_city.id),
            self._get_air_info(res_city.id),
        )
        return {
            "city": res_city.name,
            "now": res_now,
            "daily": res_daily,
            "warning": res_warning,
            "air": res_air,
        }


weather_client = Weather()
"""天气请求客户端"""
