from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.log import logger

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
"""
异步定时器，用于创建定时任务，使用方法：
```
from src.utils.scheduler import scheduler

@scheduler.scheduled_job('cron', hour=0, minute=0)
async def _():
    pass
```
"""


def start_scheduler():
    global scheduler
    if not scheduler.running:
        scheduler.start()
        logger.opt(colors=True).info("<g>定时器模块已开启。</g>")
