import asyncio
import random

from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import on, on_regex
from src.utils.browser import browser
from src.utils.log import logger
from src.utils.utils import GroupList_Async
from tortoise import Tortoise

from . import data_source as source
from ._email import mail_client
from ._jx3_event import RecvEvent, WsClosed
from ._websocket import ws_client

driver = get_driver()

# ----------------------------------------------------------------
#   bot服务的各种hook
# ----------------------------------------------------------------


@driver.on_bot_connect
async def _(bot: Bot):
    '''机器人连接处理'''
    # 获取群
    logger.info(
        f"<y>Bot {bot.self_id}</y> 已连接，正在注册……"
    )
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id: int = group['group_id']
        group_name: str = group['group_name']
        # 注册群信息
        await source.group_init(group_id, group_name)
        # 注册插件
        await source.load_plugins(group_id)
        # 注册成员信息
        member_list = await bot.get_group_member_list(group_id=group_id)
        for one_member in member_list:
            user_id = one_member['user_id']
            user_name = one_member['nickname'] if one_member['card'] == "" else one_member['card']
            await source.user_init(user_id, group_id, user_name)
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

# ----------------------------------------------------------------
#  server操作的几个mathcer
# ----------------------------------------------------------------
check_ws = on_regex(pattern=r"^查看连接$", permission=SUPERUSER, priority=5, block=True)
connect_ws = on_regex(pattern=r"^连接服务$", permission=SUPERUSER, priority=5, block=True)
close_ws = on_regex(pattern=r"^关闭连接$", permission=SUPERUSER, priority=5, block=True)


@check_ws.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''查看连接'''
    if ws_client.closed:
        msg = "jx3api > ws连接已关闭！"
    else:
        msg = "jx3api > ws连接正常！"
    await check_ws.finish(msg)


@connect_ws.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''连接服务器'''
    if ws_client.closed:
        msg = "正在连接ws服务器……"
        await connect_ws.send(msg)
        flag = await ws_client.init()
        if flag:
            msg = "连接成功！ws服务器已连接。"
        else:
            msg = "ws服务器连接失败！"
        await connect_ws.finish(msg)
    else:
        msg = "ws服务器当前已连接，不要重复连接！"
        await connect_ws.finish(msg)


@close_ws.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''关闭连接'''
    await ws_client.close()
    await close_ws.finish("ws连接已关闭！")

# ----------------------------------------------------------------
#       ws消息事件处理
# ----------------------------------------------------------------

ws_recev = on(type="WsRecv", priority=4, block=True)
ws_closed = on(type="WsClosed", priority=4, block=True)


@ws_recev.handle()
async def _(bot: Bot, event: RecvEvent):
    '''ws推送事件'''
    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        # 是否需要验证服务器
        if event.server:
            group_server = await source.get_server(group_id)
            if group_server != event.server:
                continue

        # 判断事件接受开启状态
        status = await source.get_ws_status(group_id, event)
        if status:
            try:
                await bot.send_group_msg(group_id=group_id, message=event.get_message())
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await ws_recev.finish()


@ws_closed.handle()
async def _(bot: Bot, event: WsClosed):
    '''ws关闭事件'''
    superusers = list(bot.config.superusers)
    msg = f"检测到ws链接关闭：{event.reason}\n正在重连……"
    async for user_id in GroupList_Async(superusers):
        await bot.send_private_msg(user_id=user_id, message=msg)
    flag = await ws_client.init()
    if flag:
        msg = "ws重连成功！"
    else:
        msg = "ws连接失败！"
    async for user_id in GroupList_Async(superusers):
        await bot.send_private_msg(user_id=user_id, message=msg)
    await ws_closed.finish()
