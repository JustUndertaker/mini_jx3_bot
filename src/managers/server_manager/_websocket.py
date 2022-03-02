import asyncio
import json
import time
from dataclasses import dataclass
from typing import Dict

import websockets
from httpx import AsyncClient
from nonebot import get_bots
from nonebot.message import handle_event
from src.utils.config import config
from src.utils.log import logger
from websockets.exceptions import ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol

from ._jx3_event import RecvEvent, WsClosed


@dataclass
class WsKey(object):
    status: bool = False
    '''状态'''
    time: int = 0
    '''到期时间'''

    @property
    def check(self) -> bool:
        '''检查是否过期'''
        return self.status and self.time > int(time.time())


@dataclass
class Jx3ServerStatus(object):
    '''ws服务器推送状态'''
    strategy: WsKey = WsKey()
    '''奇遇播报'''
    horse: WsKey = WsKey()
    '''抓马播报'''
    fuyao: WsKey = WsKey()
    '''扶摇播报'''


class Jx3WsTokenManager(object):
    '''wstoken管理器'''
    _data: Dict[str, Jx3ServerStatus]
    '''整体数据'''

    def __init__(self):
        self._data = {}

    def _set_key(self, data: Jx3ServerStatus, level: int, status: bool, time: int):
        if level == 1:
            data.strategy = WsKey(status, time)
        elif level == 2:
            data.horse = WsKey(status, time)
        elif level == 3:
            data.fuyao = WsKey(status, time)

    def _add_data(self, data: dict):
        '''添加数据'''
        status = data.get("status")
        server: str = data.get("server")
        level: int = data.get("level")
        time: int = data.get("time")
        # 判断server
        if server not in self._data:
            self._data[server] = Jx3ServerStatus()
        self._set_key(self._data[server], level, status, time)

    async def init(self):
        '''初始化'''
        url = config.jx3api['jx3_url'] + "/token/socket"
        params = {
            "token": config.jx3api['ws_token']
        }
        async with AsyncClient() as client:
            try:
                req = await client.get(url=url, params=params)
                req_json = req.json()
                if req_json['code'] == 200:
                    data = req_json['data']
                    for one_data in data:
                        self._add_data(one_data)
            except Exception:
                pass

    def get_data(self, server: str) -> Jx3ServerStatus:
        '''获取数据'''
        return self._data.get(server, Jx3ServerStatus())


class Jx3WebSocket(object):
    '''jx3_api的ws链接封装'''

    _ws: WebSocketClientProtocol = None
    '''ws链接'''
    _token_data: Jx3WsTokenManager = Jx3WsTokenManager()
    '''wstoekn管理器'''
    is_connecting: bool = False
    '''是否在连接中'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(Jx3WebSocket, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    async def _task(self):
        '''处理ws任务'''
        try:
            while True:
                msg = await self._ws.recv()
                asyncio.create_task(self._handle_msg(msg))

        except asyncio.CancelledError:
            pass

        except ConnectionClosedOK:
            logger.debug("<g>jx3api > ws链接已主动关闭！</g>")

        except Exception as e:
            logger.error(
                f"<r>jx3api > ws链接被关闭：{str(e)}</r>")
            await self._raise_closed(str(e))

    async def _raise_closed(self, reason: str):
        '''处理关闭事件'''
        event = WsClosed(reason)
        bots = get_bots()
        for _, one_bot in bots.items():
            await handle_event(one_bot, event)
            break  # 只发送一次

    async def _handle_msg(self, message: str):
        '''处理回复数据'''
        data: dict = json.loads(message)
        # logger.success(data)
        msg_type = data.get("type")
        if event := RecvEvent.create_event(msg_type, data.get('data')):
            logger.debug(event.log)
            bots = get_bots()
            for _, one_bot in bots.items():
                await handle_event(one_bot, event)
        else:
            logger.error(
                f"<r>未知的ws消息：{data}</r>")

    async def init(self) -> bool:
        '''初始化'''
        await self._token_data.init()
        ws_path: str = config.jx3api['ws_path']
        ws_token = config.jx3api['ws_token']
        if ws_token is None:
            ws_token = ""
        headers = {"token": ws_token}
        logger.debug(f"<g>ws_server</g> | 正在链接jx3api的ws服务器：{ws_path}")
        self.is_connecting = True
        for i in range(1, 101):
            try:
                logger.debug(
                    f"<g>ws_server</g> | 正在开始第 {i} 次尝试"
                )
                self._ws = await websockets.connect(uri=ws_path,
                                                    extra_headers=headers,
                                                    ping_interval=20,
                                                    ping_timeout=20,
                                                    close_timeout=10)
                self.is_connecting = False
                asyncio.create_task(self._task())
                logger.debug(
                    "<g>ws_server</g> | ws连接成功！"
                )
                return True
            except Exception as e:
                logger.error(
                    f"<r>链接到ws服务器时发生错误：{str(e)}</r>")
                asyncio.sleep(1)
        self.is_connecting = False
        return False

    async def close(self):
        '''关闭ws链接'''
        if self._ws:
            await self._ws.close()

    def get_ws_status(self, server: str) -> dict:
        '''获取ws状态'''
        data = self._token_data.get_data(server)
        return {
            "closed": self.closed,
            "serendipity": data.strategy.check,
            "horse": data.horse.check,
            "fuyao": data.fuyao.check
        }

    @property
    def closed(self) -> bool:
        '''ws是否关闭'''
        if self._ws:
            return self._ws.closed
        return True


ws_client = Jx3WebSocket()
"""
ws客户端，用于连接jx3api的ws服务器.

他在init连接到ws服务器后，在接受到的ws消息自动实例化为event事件并处理。
在ws服务器关闭后，会自动重连。

使用方式：
```
>>>await ws_client.init() # 初始化
>>>ws_client.closed # ws是否关闭
>>>ws_client.get_ws_status() # 获取ws状态
>>>await ws_client.close() # 关闭
```
"""
