from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .log import logger

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
'''全局定时器对象'''


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("<g>定时器模块已开启。</g>")
