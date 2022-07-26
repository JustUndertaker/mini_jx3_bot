import random

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from src.params import PluginConfig, cost_gold

from .config import GUAXIANG
from .model import Quadrant

__plugin_meta__ = PluginMetadata(
    name="算卦",
    description="使用梅花易数进行占卜，简易解卦",
    usage="算一卦 | 算卦",
    config=PluginConfig(cost_gold=5),
)

suangua = on_regex(pattern=r"^算(一){0,1}卦$", permission=GROUP, priority=5, block=True)


@suangua.handle(parameterless=[cost_gold(gold=5)])
async def _(bot: Bot, event: GroupMessageEvent):

    msg = "起卦中..."
    await suangua.send(MessageSegment.at(event.user_id) + msg)

    msg = get_forward_msg(bot_id=bot.self_id, nickname=list(bot.config.nickname)[0])
    await bot.send_group_forward_msg(group_id=event.group_id, messages=msg)
    await suangua.finish()


def get_forward_msg(bot_id: str, nickname: str) -> list[dict]:
    """获取消息内容"""
    chain = []
    # 起卦
    up_value = random.randint(1, 100000)
    down_value = random.randint(1, 100000)
    bengua = Quadrant.start(up_value, down_value)
    guajie_ben = bengua.get_exception()
    msg = f"体卦：{bengua.get_tigua()} \n用卦：{bengua.get_yonggua()}\n动爻：{bengua.dong_yao}"
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    # 互卦
    hugua = bengua.get_hugua()
    guajie_hu = hugua.get_exception()
    # 变卦
    biangua = bengua.get_biangua()
    guajie_bian = biangua.get_exception()
    msg = (
        f"本卦：\n上：{bengua.up_quadrant} 下：{bengua.down_quadrant} 卦解：{guajie_ben}"
        f"\n互卦：\n上：{hugua.up_quadrant} 下：{hugua.down_quadrant} 卦解：{guajie_hu}"
        f"\n变卦：\n上：{biangua.up_quadrant} 下：{biangua.down_quadrant} 卦解：{guajie_bian}"
    )
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    msg = (
        "卦解(以求事为例):\n"
        f"开端：{guajie_ben.get_qiumou()}\n"
        f"发展：{guajie_hu.get_qiumou()}\n"
        f"结局：{guajie_bian.get_qiumou()}"
    )
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    msg = "---------卦辞--------"
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    # 卦辞
    xiang_ben = GUAXIANG[bengua.up_quadrant.name][bengua.down_quadrant.name]
    msg = f"本卦：\n{xiang_ben['description']}"
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    xiang_hu = GUAXIANG[hugua.up_quadrant.name][hugua.down_quadrant.name]
    msg = f"互卦：\n{xiang_hu['description']}"
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    xiang_bian = GUAXIANG[biangua.up_quadrant.name][biangua.down_quadrant.name]
    msg = f"变卦：\n{xiang_bian['description']}"
    data = {
        "type": "node",
        "data": {
            "name": nickname,
            "uin": bot_id,
            "content": msg,
        },
    }
    chain.append(data)

    return chain
