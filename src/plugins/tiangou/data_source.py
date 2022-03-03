from datetime import datetime
from typing import Optional

from httpx import AsyncClient
from src.utils.config import config
from src.utils.log import logger


async def get_tiangou() -> Optional[str]:
    '''
    :说明
        获取一条舔狗日记

    :返回
        * `str`：获取内容
        * `None`：转换出错
    '''
    jx3_url: str = config.jx3api['jx3_url']
    url = f"{jx3_url}/realize/random"

    async with AsyncClient() as client:
        try:
            req_url = await client.get(url=url)
            req = req_url.json()
            if req['code'] == 200:
                data = req['data']
                text = data['text']
                log = f"<g>舔狗日记</g> | 请求日记成功：{text}"
                logger.debug(log)
                date_now = datetime.now()
                date_str = date_now.strftime('%Y年%m月%d日')
                req_text = date_str+"\n"+text
                return req_text
            else:
                log = f'<g>舔狗日记</g> | 请求日记出错：{req["msg"]}'
                logger.debug(log)
                return None
        except Exception as e:
            log = f'<g>舔狗日记</g> | 请求链接失败，原因：{str(e)}'
            logger.error(log)
            return None
