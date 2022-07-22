from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent
from nonebot.plugin import PluginMetadata

from src.modules.group_info import GroupInfo
from src.params import PluginConfig
from src.utils.log import logger
from src.utils.scheduler import scheduler

from .data_source import get_sign_in

__plugin_meta__ = PluginMetadata(
    name="每日签到",
    description="简单签到插件，每天只能签到一次噢。",
    usage="签到",
    config=PluginConfig(),
)


sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(event: GroupMessageEvent):
    """签到系统"""
    user_id = event.user_id
    group_id = event.group_id
    logger.info(f"<y>群{group_id}</y> | <g>{user_id}</g> | 请求签到")
    msg = await get_sign_in(user_id, group_id)
    await sign.finish(msg)


@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    """每天零点重置签到人数"""
    logger.info("正在重置签到人数")
    await GroupInfo.reset_sign_nums()
    logger.info("签到人数已重置")
