"""
jx3api接口的实现，用于连接api网站的数据处理
"""

from functools import partial
from typing import Any, Optional

from httpx import AsyncClient
from pydantic import BaseModel
from src.utils.config import Config as BaseConfig
from typing_extensions import Protocol


class _ApiCall(Protocol):
    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Config(BaseModel):
    '''jx3api的设置'''
    ws_path: str
    '''ws链接地址'''
    ws_token: Optional[str]
    '''wstoken，按需购买'''
    jx3_url: str
    '''jx3api主站地址'''
    jx3_token: Optional[str]
    '''jx3api主站token，按需购买'''


class Response(BaseModel):
    '''返回数据模型'''
    code: int
    '''状态码'''
    msg: str
    '''返回消息字符串'''
    data: dict | list[dict]
    '''返回数据'''
    time: int
    '''时间戳'''


class JX3API:
    '''
    jx3api接口类，负责访问网站接口，获取数据。
    '''
    client: AsyncClient
    '''浏览器客户端'''
    config: Config
    '''api设置'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(JX3API, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        base_config = BaseConfig()
        self.config = Config.parse_obj(base_config.jx3api)
        if not self.config.jx3_url.endswith("/"):
            self.config.jx3_url += "/"
        token = self.config.jx3_token or ""
        headers = {"token": token, "User-Agent": "Nonebot2-jx3_bot"}
        self.client = AsyncClient(headers=headers)

    async def call_api(self, url: str, **data: Any) -> Response:
        '''请求api网站数据'''
        try:
            res = await self.client.get(url=url, params=data)
            return Response.parse_obj(res.json())
        except Exception as e:
            return Response(
                code=0,
                msg=f"{str(e)}",
                data={},
                time=0
            )

    def __getattr__(self, name: str) -> _ApiCall:
        # 拼接url
        url = self.config.jx3_url + name.replace("_", "/")
        return partial(self.call_api, url)
