"""
nlp聊天实现，用于自动回复
"""

from typing import Optional

from httpx import AsyncClient

from src.config import nlp_config, voice_config
from src.utils.log import logger

from .jx3api import JX3API, Response


class NLP:
    """
    nlp封装类
    """

    client: AsyncClient
    """异步请求客户端"""
    qingyunke_url: str
    """青云客接口地址"""

    def __init__(self):
        self.client = AsyncClient()
        self.api = JX3API()
        self.nlp_config = nlp_config
        self.voice_config = voice_config
        self.qingyunke_url = "http://api.qingyunke.com/api.php"

    def check_nlp_config(self) -> bool:
        """
        检查nlp配置
        """
        return self.nlp_config.secretId != "" and self.nlp_config.secretKey != ""

    def check_voice_config(self) -> bool:
        """
        检查voice配置
        """
        return self.voice_config.access != "" and self.voice_config.appkey != ""

    async def chat_with_tencent(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            使用腾讯云接口聊天

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        try:
            req: Response = await self.api.data_chat_tencent(
                secretId=self.nlp_config.secretId,
                secretKey=self.nlp_config.secretKey,
                name=nickname,
                question=text,
            )
            if req.code == 200:
                msg: str = req.data["answer"]
                logger.debug(f"腾讯请求成功，返回：{msg}")
                return msg
            else:
                return None
        except Exception as e:
            logger.debug(f"腾讯云请求错误，返回：{str(e)}")
            return None

    async def chat_with_qingyunke(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            使用青云客接口聊天

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        params = {"key": "free", "appid": 0, "msg": text}
        try:
            req = await self.client.get(self.qingyunke_url, params=params)
            req_json = req.json()
            if req_json["result"] == 0:
                msg = str(req_json["content"])
                # 消息替换
                msg = msg.replace(r"{br}", "\n")
                msg = msg.replace("菲菲", nickname)
                logger.debug(f"青云客请求成功，返回：{msg}")
                return msg
            else:
                logger.debug(f"青云客请求失败，返回：{req_json['content']}")
                return None
        except Exception as e:
            logger.debug(f"青云客请求出错，返回：{str(e)}")
            return None

    async def chat(self, nickname: str, text: str) -> Optional[str]:
        """
        说明:
            请求聊天，优先使用腾讯云接口

        参数:
            * `nickname`：机器人昵称
            * `text`：聊天内容

        返回:
            * `str`：回复内容
        """
        if self.check_nlp_config():
            if msg := await self.chat_with_tencent(nickname, text):
                return msg
        return await self.chat_with_qingyunke(nickname, text)

    async def get_voice(self, text: str) -> Optional[str]:
        """
        说明:
            使用阿里云文字转语音

        参数:
            * `text`：转换语音内容

        返回:
            * `str`：语音url地址
        """
        logger.debug(f"请求语音合成：{text}")
        try:
            req: Response = await self.api.data_voice_alitts(
                text=text, **self.voice_config
            )
            if req.code == 200:
                logger.debug("请求语音成功！")
                return req.data["url"]
            else:
                logger.debug(f"请求语音失败，返回：{req.data}")
                return None
        except Exception as e:
            logger.debug(f"语音合成出错，返回：{str(e)}")
            return None


chat = NLP()
"""
nlp聊天封装，用于自动回复
"""
