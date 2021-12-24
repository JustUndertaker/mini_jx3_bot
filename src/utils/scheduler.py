from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.log import logger
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    apscheduler_config: dict = Field(
        default_factory=lambda: {"apscheduler.timezone": "Asia/Shanghai"})

    class Config:
        extra = "ignore"


plugin_config = Config()

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
'''全局定时器对象'''


async def start_scheduler():
    if not scheduler.running:
        scheduler.configure(plugin_config.apscheduler_config)
        scheduler.start()
        logger.opt(colors=True).info("<y>定时器模块已开启。</y>")
