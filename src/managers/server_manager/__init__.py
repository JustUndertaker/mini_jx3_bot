from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from src.utils.browser import browser
from src.utils.log import logger
from tortoise import Tortoise

from . import data_source as source
from ._email import mail_client
from ._websocket import ws_client

driver = get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    '''机器人连接处理'''
    # 获取群
    logger.info(
        f"<y>Bot {bot.self_id}</y> 已连接，正在注册……"
    )
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group['group_id']
        group_name = group['group_name']
        # 注册群信息
        await source.group_init(group_id, group_name)
        # 注册插件
        await source.load_plugins(group_id)
    logger.info(
        f"<y>Bot {bot.self_id}</y> 注册完毕。"
    )


@driver.on_bot_disconnect
async def _(bot: Bot):
    '''bot链接关闭'''
    bot_id = bot.self_id
    logger.info("<y>检测到bot离线，发送通知邮件……</y>")
    await mail_client.send_mail(bot_id)


@driver.on_startup
async def _():
    '''等定时插件和数据加载完毕后'''
    logger.info("<g>正在初始化浏览器……</g>")
    await browser.init()
    logger.info("<y>浏览器初始化完毕。</y>")
    logger.info("<g>正在链接jx3api的ws服务器……</g>")
    await ws_client.init()
    logger.info("<y>jx3api的ws服务器已链接。</y>")


@driver.on_shutdown
async def _():
    '''结束进程'''
    logger.info("检测到进程关闭，正在清理……")
    logger.info("<y>正在关闭浏览器……</y>")
    await browser.shutdown()
    logger.info("<g>浏览器关闭成功。</g>")

    logger.info("<y>正在关闭数据库……</y>")
    await Tortoise.close_connections()
    logger.info("<g>数据库关闭成功。</g>")

    logger.info("<y>关闭ws链接……</y>")
    await ws_client.close()
    logger.info("<g>ws链接关闭成功。</g>")
