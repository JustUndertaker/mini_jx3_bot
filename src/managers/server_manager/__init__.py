from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot
from src.utils.browser import browser
from src.utils.log import logger
from tortoise import Tortoise

from ._email import mail_client
from ._websocket import ws_client

driver = get_driver()


# TODO:Bot是基类，后续需要更换
@driver.on_bot_disconnect
async def _(bot: Bot):
    '''bot链接关闭'''
    bot_id = bot.self_id
    logger.opt(colors=True).info("<y>检测到bot离线，发送通知邮件……</y>")
    await mail_client.send_mail(bot_id)


@driver.on_startup
async def _():
    '''等定时插件和数据加载完毕后'''
    logger.opt(colors=True).info("<g>正在初始化浏览器……</g>")
    await browser.init()
    logger.opt(colors=True).info("<y>浏览器初始化完毕。</y>")
    logger.opt(colors=True).info("<g>正在链接jx3api的ws服务器……</g>")
    await ws_client.init()
    logger.opt(colors=True).info("<y>jx3api的ws服务器已链接。</y>")


@driver.on_shutdown
async def _():
    '''结束进程'''
    logger.info("检测到进程关闭，正在清理……")
    logger.opt(colors=True).info("<y>正在关闭浏览器……</y>")
    await browser.shutdown()
    logger.opt(colors=True).info("<g>浏览器关闭成功。</g>")
    logger.opt(colors=True).info("<y>正在关闭数据库……</y>")
    # await Tortoise.close_connections()
    logger.opt(colors=True).info("<g>数据库关闭成功。</g>")
    logger.opt(colors=True).info("<y>关闭ws链接……</y>")
    await ws_client.close()
    logger.opt(colors=True).info("<g>ws链接关闭成功。</g>")
