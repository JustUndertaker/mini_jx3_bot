import random
from typing import Optional

from nonebot.adapters.onebot.v11.message import MessageSegment
from src.modules.group_info import GroupInfo

from .model import chat


async def _get_active(group_id: int) -> int:
    '''获取活跃值'''
    return await GroupInfo.get_bot_active(group_id)


async def get_random_msg(group_id: int, nickname: str, text: str) -> Optional[MessageSegment]:
    '''获取随机返回值'''
    active = await _get_active(group_id)
    random_num = random.uniform(0, 200)
    if random_num > active:
        return None

    msg = await chat.chat(nickname, text)
    if not msg:
        return None

    random_num = random.uniform(0, 100)
    if random_num < 33:
        if chat.check_voice_config():
            voice = await chat.get_voice(msg)
            if voice:
                return MessageSegment.record(file=voice)
    return MessageSegment.text(msg)
