"""
jx3api接口的实现，用于连接api网站的数据处理
"""

from functools import partial
from typing import Any, Optional

from httpx import AsyncClient
from pydantic import BaseModel
from typing_extensions import Protocol

from src.config import Jx3ApiConfig, jx3api_config
from src.utils.log import logger

SERVER_DICT = {
    "长安城": ["长安城", "长安"],
    "龙争虎斗": ["龙争虎斗", "龙虎"],
    "蝶恋花": ["蝶恋花", "蝶服"],
    "剑胆琴心": ["剑胆琴心", "剑胆", "煎蛋", "剑胆金榜", "侠者成歌"],
    "幽月轮": ["幽月轮", "六合一", "七合一"],
    "乾坤一掷": ["乾坤一掷", "华乾"],
    "斗转星移": ["斗转星移", "姨妈", "风雨大姨妈", "姨妈服", "大唐万象"],
    "唯我独尊": ["唯我独尊", "唯满侠", "鹅服"],
    "梦江南": ["梦江南", "双梦镇", "双梦"],
    "绝代天骄": ["绝代天骄", "绝代", "电八"],
    "天鹅坪": ["天鹅坪", "纵月", "纵月六只鹅", "双剑"],
    "破阵子": ["破阵子", "念破"],
    "飞龙在天": ["飞龙在天", "飞龙", "双二"],
    "青梅煮酒": ["青梅煮酒", "青梅", "双四"],
    "横刀断浪": ["横刀断浪", "电五"],
}
"""区服列表"""


class _ApiCall(Protocol):
    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: dict | list[dict]
    """返回数据"""
    time: int
    """时间戳"""


class JX3API:
    """
    jx3api接口类，负责访问网站接口，获取数据。
    """

    client: AsyncClient
    """浏览器客户端"""
    config: Jx3ApiConfig
    """api设置"""

    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, "_instance"):
            orig = super(JX3API, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.config = jx3api_config
        if not self.config.api_url.endswith("/"):
            self.config.api_url += "/"
        token = self.config.api_token or ""
        headers = {"token": token, "User-Agent": "Nonebot2-jx3-bot"}
        self.client = AsyncClient(headers=headers)

    def app_server(self, *, name: str) -> Optional[str]:
        """
        说明:
            主从大区

        参数:
            * `name`：大区名称

        返回:
            * `str`：主区名称
        """
        for key, value in SERVER_DICT.items():
            if name in value:
                return key
        return None

    async def call_api(self, url: str, **data: Any) -> Response:
        """请求api网站数据"""
        try:
            res = await self.client.get(url=url, params=data)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>jx3api请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)

    def __getattr__(self, name: str) -> _ApiCall:
        # 拼接url
        logger.debug(f"<y>jx3api请求功能:</y> | {name}")
        url = self.config.api_url + name.replace("_", "/")
        return partial(self.call_api, url)
