from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.plugin import get_loaded_plugins

chat = on_regex(pattern=r'^测试$', priority=1, block=True)


@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    plugin = get_loaded_plugins()
    a = 1
