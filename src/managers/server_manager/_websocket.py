import asyncio
import json

import websockets
from src.utils.config import config
from src.utils.log import logger
from websockets.exceptions import ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol


class Jx3WebSocket(object):
    '''jx3_api的ws链接封装'''

    _ws: WebSocketClientProtocol = None
    '''ws链接'''

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
            logger.opt(colors=True).debug("<g>jx3api > ws链接已主动关闭！</g>")

        except Exception as e:
            logger.opt(colors=True).error(
                f"<r>jx3api > ws链接被关闭：{str(e)}</r>")

    async def _handle_msg(self, message: str):
        '''处理回复数据'''
        data = json.loads(message)
        logger.success(f"收到ws推送消息：{str(data)}")
        # msg_type: int = data['type']
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
            logger.opt(colors=True).error(
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
