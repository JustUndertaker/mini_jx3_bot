from typing import Optional

from httpx import AsyncClient
from src.utils.config import config
from src.utils.log import logger


class Chat(object):
    '''聊天封装'''
    _client = None
    '''异步客户端'''
    _tencent_url: str
    '''腾讯云接口'''
    _voice_url: str
    '''语音请求接口'''
    _qingyunke_url = "http://api.qingyunke.com/api.php"
    '''青云客接口'''
    _nlp_config: dict
    '''nlp配置'''
    _voice_config: dict
    '''voice配置'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(Chat, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._client = AsyncClient()
        base_url = config.jx3api['jx3_url']
        self._tencent_url = base_url+"/realize/nlpchat"
        self._voice_url = base_url+"/realize/alitts"
        self._nlp_config = config.nlp
        self._voice_config = config.voice

    def _check_nlp_config(self) -> bool:
        '''检查nlp配置'''
        return (self._nlp_config.get("secretId") is not None) and (self._nlp_config.get("secretKey") is not None)

    async def _chat_with_tencent(self, nickname: str, text: str) -> Optional[str]:
        '''使用腾讯云接口'''
        params = self._nlp_config.copy()
        params['name'] = nickname
        params['question'] = text
        try:
            req = await self._client.get(url=self._tencent_url, params=params)
            req_json = req.json()
            if req_json['code'] == 200:
                data = req_json['data']
                logger.debug(
                    f"腾讯云请求成功，返回：{data['answer']}"
                )
                return data['answer']
            else:
                logger.debug(
                    f"腾讯云请求失败，返回：{req_json['msg']}"
                )
                return None
        except Exception as e:
            logger.debug(
                f"腾讯云请求错误，返回：{str(e)}"
            )
            return None

    async def _chat_with_qingyunke(self, nickname: str, text: str) -> Optional[str]:
        '''使用青云客api聊天'''
        params = {
            "key": "free",
            "appid": 0,
            "msg": text
        }
        try:
            req = await self._client.get(url=self._qingyunke_url, params=params)
            req_json = req.json()
            if req_json['result'] == 0:
                msg = str(req_json['content'])
                # 消息替换
                msg = msg.replace(r'{br}', '\n')
                msg = msg.replace('菲菲', nickname)
                logger.debug(
                    f"青云客请求成功，返回：{msg}"
                )
                return msg
            else:
                logger.debug(
                    f"青云客请求失败，返回：{req_json['content']}"
                )
                return None
        except Exception as e:
            logger.debug(
                f"青云客请求出错，返回：{str(e)}"
            )
            return None

    async def chat(self, nickname: str, text: str) -> Optional[str]:
        '''请求聊天，优先使用腾讯云'''
        flag = self._check_nlp_config()
        if flag:
            msg = await self._chat_with_tencent(nickname, text)
            if msg:
                return msg
        msg = await self._chat_with_qingyunke(nickname, text)
        if msg:
            return msg
        return None

    def check_voice_config(self) -> bool:
        '''检查voice的配置是否齐全'''
        return (self._voice_config.get("appkey") is not None) and (self._voice_config.get("access") is not None) and (self._voice_config.get("secret") is not None)

    async def get_voice(self, text: str) -> Optional[str]:
        '''获取语音'''
        logger.debug(f"请求语音合成：{text}")
        params = self._voice_config.copy()
        params['text'] = text
        try:
            req = await self._client.get(url=self._voice_url, params=params)
            req_json = req.json()
            if req_json['code'] == 200:
                logger.debug("请求语音成功！")
                data = req_json['data']
                voice_url = data['url']
                return voice_url
            else:
                logger.debug(f"请求语音失败，返回：{req_json['msg']}")
                return None

        except Exception as e:
            logger.debug(
                f"请求语音出错，返回：{str(e)}"
            )
            return None


chat = Chat()
'''聊天请求器'''
