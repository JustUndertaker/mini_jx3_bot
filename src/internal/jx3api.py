"""
jx3api接口的实现，用于连接api网站的数据处理
"""

from functools import partial
from typing import Any

from httpx import AsyncClient
from pydantic import BaseModel
from typing_extensions import Protocol

from src.config import Jx3ApiConfig, jx3api_config
from src.utils.log import logger


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
        headers = {"token": token, "User-Agent": "Nonebot2-jx3_bot"}
        self.client = AsyncClient(headers=headers)

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
        url = self.config.api_url + name.replace("_", "/", 1)
        return partial(self.call_api, url)
