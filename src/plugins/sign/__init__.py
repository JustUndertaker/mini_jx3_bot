from nonebot import export, on_regex
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP

from . import data_source as source

Export = export()
Export.plugin_name = "每日签到"
Export.plugin_command = "签到"
Export.plugin_usage = "简单签到插件，每天只能签到一次噢。"
Export.default_status = True


sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''签到系统'''
    user_id = event.user_id
    group_id = event.group_id
    msg = await source.get_sign_in(user_id, group_id)
    await sign.finish(msg)
