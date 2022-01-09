import asyncio
import json

import websockets
from nonebot import get_bots
from nonebot.message import handle_event
from src.utils.config import config
from src.utils.log import logger
from websockets.exceptions import ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol

from ._jx3_event import ws_event_factory


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

    async def _handle_msg(self, message: str):
        '''处理回复数据'''
        data = json.loads(message)
        msg_type: int = data['type']
        # 判断首次信息
        if msg_type == 10000:
            self._handle_first_recv(data['data'])
        else:
            # 分发事件
            event = ws_event_factory(msg_type, data['data'])
            logger.debug(event.log)
            if event:
                bots = get_bots()
                for _, one_bot in bots.items():
                    await handle_event(one_bot, event)

    def _handle_first_recv(self, data: dict[str, str]):
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

    async def init(self):
        '''初始化'''
        ws_path: str = config.jx3api['ws_path']
        logger.debug(f"正在链接jx3api的ws服务器：{ws_path}")
        try:
            self._ws = await websockets.connect(uri=ws_path,
                                                ping_interval=20,
                                                ping_timeout=20,
                                                close_timeout=10)
            asyncio.create_task(self._task())

        except Exception as e:
            logger.error(
                f"<r>链接到ws服务器时发生错误：{str(e)}</r>")

    async def close(self):
        '''关闭ws链接'''
        if self._ws:
            await self._ws.close()

    @property
    def closed(self) -> bool:
        '''ws是否关闭'''
        return self._ws.closed


ws_client = Jx3WebSocket()
'''ws客户端'''
