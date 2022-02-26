import asyncio
import json
from typing import Dict

import websockets
from nonebot import get_bots
from nonebot.message import handle_event
from src.utils.config import config
from src.utils.log import logger
from websockets.exceptions import ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol

from ._jx3_event import RecvEvent, WsClosed


class Jx3WebSocket(object):
    '''jx3_api的ws链接封装'''

    _ws: WebSocketClientProtocol = None
    '''ws链接'''
    _open_server: bool = False
    '''开服监控'''
    _news: bool = False
    '''官方资讯'''
    _serendipity: bool = False
    '''奇遇播报'''
    _horse: bool = False
    '''抓马播报'''
    _fuyao: bool = False
    '''扶摇播报'''
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
        # 判断首次信息
        if (msg_type := data['type']) == 10000:
            msg_type: int

            self._handle_first_recv(data['data'])
        else:
            # 分发事件
            if event := RecvEvent.create_event(msg_type, data['data']):
                logger.debug(event.log)
                bots = get_bots()
                for _, one_bot in bots.items():
                    await handle_event(one_bot, event)
            else:
                logger.error(
                    f"<r>未知的ws消息：{data}</r>")

    def _handle_first_recv(self, data: Dict[str, str]):
        '''处理首次接收事件'''
        def _to_bool(string: str) -> bool:
            return (string == "已开启")
        try:
            self._open_server = _to_bool(data['开服监控'])
            self._news = _to_bool(data['官方资讯'])
            self._serendipity = _to_bool(data['奇遇播报'])
            self._horse = _to_bool(data['抓马播报'])
            self._fuyao = _to_bool(data['扶摇播报'])
        except Exception:
            pass

    async def init(self) -> bool:
        '''初始化'''
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

    def get_ws_status(self) -> dict:
        '''获取ws状态'''
        return {
            "closed": self.closed,
            "open_server": self._open_server,
            "news": self._news,
            "serendipity": self._serendipity,
            "horse": self._horse,
            "fuyao": self._fuyao
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
