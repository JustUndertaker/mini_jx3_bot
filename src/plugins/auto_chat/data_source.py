import random
from typing import Optional

from nonebot.adapters.onebot.v11.message import MessageSegment

from src.internal.nlp import chat
from src.utils.log import logger


async def get_random_msg(
    group_id: int, nickname: str, text: str
) -> Optional[MessageSegment]:
    """获取随机返回值"""
    logger.info(f"<y>群{group_id}</y> | 请求：{text}")
    msg = await chat.chat(nickname, text)
    if not msg:
        return None
    logger.debug(f"<y>群{group_id}</y> | 返回：{msg}")
    random_num = random.uniform(0, 100)
    if random_num < 33:
        if chat.check_voice_config():
            voice = await chat.get_voice(msg)
            if voice:
                return MessageSegment.record(file=voice)
    return MessageSegment.text(msg)
