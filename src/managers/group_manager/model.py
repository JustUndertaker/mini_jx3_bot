from pathlib import Path

from httpx import AsyncClient
from nonebot.utils import run_sync


class ImageHandler:
    """
    图片处理类，将同步储存更换为异步执行
    """

    @classmethod
    @run_sync
    def _save_image(cls, file_name: Path, data: bytes):
        """
        说明:
            将数据保存到本地
        """
        with open(file_name, mode="wb") as f:
            f.write(data)

    @classmethod
    async def save_image(cls, file_name: Path, url: str) -> bool:
        """
        说明:
            从url获取图片并保存到本地

        参数:
            * `file_name`：保存的图片路径
            * `url`：图片url地址

        返回:
            * `bool`：保存是否成功
        """
        async with AsyncClient() as client:
            try:
                req = await client.get(url=url)
                await cls._save_image(file_name, req.read())
                return True
            except Exception:
                return False

    @classmethod
    @run_sync
    def load_image(cls, file_name: Path) -> bytes:
        """
        说明:
            从本地读取图片数据

        参数:
            * `file_name`：图片路径

        返回:
            * `bytes`：图片数据
        """
        with open(file_name, "rb") as f:
            data = f.read()
        return data
