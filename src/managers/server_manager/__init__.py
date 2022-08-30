import asyncio
import random

from nonebot import get_driver, on
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent
from nonebot.plugin import PluginMetadata
from tortoise import Tortoise

from src.internal.plugin_manager import plugin_manager
from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo
from src.params import PluginConfig, admin_matcher_group
from src.utils.browser import browser
from src.utils.log import logger
from src.utils.utils import GroupList_Async

from ._jx3_event import RecvEvent, WsNotice
from .data_source import get_ws_status, ws_init
from .jx3_websocket import ws_client

__plugin_meta__ = PluginMetadata(
    name="服务管理插件",
    description="管理bot的启动连接服务，以及jx3api的ws管理",
    usage="本插件不受插件管理器限制",
    config=PluginConfig(enable_managed=False),
)


driver = get_driver()

# ----------------------------------------------------------------
#   bot服务的各种hook
# ----------------------------------------------------------------


@driver.on_bot_connect
async def _(bot: Bot):
    """机器人连接处理"""
    # 获取群
    logger.info(f"<y>Bot {bot.self_id}</y> 已连接，正在注册...")
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id: int = group["group_id"]
        group_name: str = group["group_name"]
        # 注册群信息
        await GroupInfo.group_init(group_id, group_name)
        # 注册插件
        await plugin_manager.load_plugins(group_id)
        # 注册成员信息
        member_list = await bot.get_group_member_list(group_id=group_id)
        for one_member in member_list:
            user_id = one_member["user_id"]
            user_name = (
                one_member["nickname"]
                if one_member["card"] == ""
                else one_member["card"]
            )
            await UserInfo.user_init(user_id, group_id, user_name)
    logger.info(f"<y>Bot {bot.self_id}</y> 注册完毕。")


@driver.on_bot_disconnect
async def _(bot: Bot):
    """bot链接关闭"""
    logger.info("<y>检测到bot离线...</y>")


@driver.on_startup
async def _():
    """等定时插件和数据加载完毕后"""
    logger.info("<g>正在初始化浏览器...</g>")
    await browser.init()
    logger.info("<y>浏览器初始化完毕。</y>")
    asyncio.create_task(ws_init())
    # scheduler.add_job(func=ws_init, next_run_time=datetime.now() + timedelta(seconds=2))


@driver.on_shutdown
async def _():
    """结束进程"""
    logger.info("检测到进程关闭，正在清理...")
    logger.info("<y>正在关闭浏览器...</y>")
    await browser.shutdown()
    logger.info("<g>浏览器关闭成功。</g>")

    logger.info("<y>正在关闭数据库...</y>")
    await Tortoise.close_connections()
    logger.info("<g>数据库关闭成功。</g>")

    logger.info("<y>关闭ws链接...</y>")
    await ws_client.close()
    logger.info("<g>ws链接关闭成功。</g>")


# ----------------------------------------------------------------
#  server操作的几个mathcer
# ----------------------------------------------------------------
check_ws = admin_matcher_group.on_regex(pattern=r"^查看连接$")
connect_ws = admin_matcher_group.on_regex(pattern=r"^连接服务$")
close_ws = admin_matcher_group.on_regex(pattern=r"^关闭连接$")


@check_ws.handle()
async def _(event: PrivateMessageEvent):
    """查看连接"""
    if ws_client.closed:
        msg = "jx3api > ws连接已关闭！"
    else:
        msg = "jx3api > ws连接正常！"
    await check_ws.finish(msg)


@connect_ws.handle()
async def _(event: PrivateMessageEvent):
    """连接服务器"""
    if not ws_client.closed:
        await connect_ws.finish("连接正常，请不要重复连接。")

    if ws_client.is_connecting:
        await connect_ws.finish("正在连接中，请不要重复连接。")

    await connect_ws.send("正在连接服务器...")
    flag = await ws_client.init()
    msg = None
    if flag:
        msg = "jx3api > ws已连接！"
    await connect_ws.finish(msg)


@close_ws.handle()
async def _(event: PrivateMessageEvent):
    """关闭连接"""
    if not ws_client.closed:
        await ws_client.close()
    await close_ws.finish()


# ----------------------------------------------------------------
#       ws消息事件处理
# ----------------------------------------------------------------

ws_recev = on(type="WsRecv", priority=2, block=True)
ws_notice = on(type="WsNotice", priority=2, block=True)


@ws_recev.handle()
async def _(bot: Bot, event: RecvEvent):
    """ws推送事件"""
    group_list = await bot.get_group_list()
    async for group_id in GroupList_Async(group_list):
        # 是否需要验证服务器
        if event.server:
            group_server = await GroupInfo.get_server(group_id)
            if group_server != event.server:
                continue

        # 判断事件接受开启状态
        status = await get_ws_status(group_id, event)
        if status:
            try:
                await bot.send_group_msg(group_id=group_id, message=event.get_message())
                await asyncio.sleep(random.uniform(0.3, 0.5))
            except Exception:
                pass
    await ws_recev.finish()


@ws_notice.handle()
async def _(bot: Bot, event: WsNotice):
    """ws通知主人事件"""
    superusers = list(bot.config.superusers)
    msg = event.message
    async for user_id in GroupList_Async(superusers):
        await bot.send_private_msg(user_id=user_id, message=msg)
    await ws_notice.finish()
