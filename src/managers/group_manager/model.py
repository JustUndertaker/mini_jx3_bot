from pathlib import Path

from httpx import AsyncClient
from nonebot.utils import run_sync


class ImageHandler(object):
    '''图片处理类，将同步储存更换为异步执行'''

    @classmethod
    @run_sync
    def _save_image(cls, file_name: Path, data: bytes):
        '''储存图片'''
        with open(file_name, mode='wb') as f:
            f.write(data)

    @classmethod
    async def save_image(cls, file_name: Path, url: str) -> bool:
        '''储存图片'''
        async with AsyncClient() as client:
            try:
                req = await client.get(url=url)
                await cls._save_image(file_name, req.read())
                return True
            except Exception:
                return False

    @classmethod
    @run_sync
    def load_image(cls, file_name: str) -> bytes:
        '''读取图片'''
        with open(file_name, 'rb') as f:
            data = f.read()
        return data
