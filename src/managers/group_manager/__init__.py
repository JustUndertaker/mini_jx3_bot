import asyncio
import random
import time

from nonebot import get_bots, on_notice, on_regex
from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendAddNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupMessageEvent,
    Message,
    MessageSegment,
    PokeNotifyEvent,
)
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import Depends, RegexDict
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

from src.internal.jx3api import JX3API
from src.internal.plugin_manager import plugin_manager
from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo
from src.params import GROUP_ADMIN, GroupSetting, NoticeType, PluginConfig
from src.utils.browser import browser
from src.utils.log import logger
from src.utils.scheduler import scheduler
from src.utils.utils import GroupList_Async

from . import data_source as source

__plugin_meta__ = PluginMetadata(
    name="群管理插件",
    description="""
        群管理插件，实现功能有：
        * 绑定服务器
        * 设置活跃值
        * 机器人开关
        * 晚安通知，进群通知，离群通知
        * 菜单
        * 管理员帮助
        * 滴滴
        """,
    usage="参考“管理员帮助”指令",
    config=PluginConfig(enable_managed=False),
)

api = JX3API()

# 绑定服务器
bind_server = on_regex(
    pattern=r"^绑定 (?P<value>[\u4e00-\u9fa5]+)$",
    permission=SUPERUSER | GROUP_ADMIN,
    priority=2,
    block=True,
)

# 设置活跃值[0-99]
set_activity = on_regex(
    pattern=r"^活跃值 (?P<value>(\d){1,2})$",
    permission=SUPERUSER | GROUP_ADMIN,
    priority=2,
    block=True,
)

# 设置机器人开关
robot_status = on_regex(
    pattern=r"^机器人 (?P<command>[开关])$",
    permission=SUPERUSER | GROUP_ADMIN,
    priority=2,
    block=True,
)

# 晚安通知，离群通知，进群通知
notice = on_regex(
    pattern=r"^((晚安)|(离群)|(进群))通知 ",
    permission=SUPERUSER | GROUP_ADMIN,
    priority=2,
    block=True,
)

# 菜单
meau = on_regex(pattern=r"^((菜单)|(状态))$", permission=GROUP, priority=3, block=True)

# 管理员帮助
admin_help = on_regex(pattern=r"^管理员帮助$", permission=GROUP, priority=3, block=True)

# 滴滴
didi = on_regex(pattern=r"^滴滴 ", permission=GROUP_ADMIN, priority=3, block=True)

# 通知事件
get_notice = on_notice(priority=3, block=True)

# -------------------------------------------------------------
#   Depends依赖
# -------------------------------------------------------------


def get_value(regex_dict: dict = RegexDict()) -> str:
    """
    说明:
        Dependcey，获取value值

    返回:
        * `value`：value值
    """
    return regex_dict["value"]


def get_status(regex_dict: dict = RegexDict()) -> bool:
    """
    说明:
        Dependcey，获取命令中的开关

    返回:
        * `bool`：命令开关
    """
    return regex_dict["command"] == "开"


def get_notice_type(event: GroupMessageEvent) -> NoticeType:
    """
    说明:
        Dependcey，返回通知类型

    返回:
        * `NoticeType`：通知类型枚举
    """
    msg = event.get_plaintext()[:4]
    match msg:
        case "晚安通知":
            return NoticeType.晚安通知
        case "离群通知":
            return NoticeType.离群通知
        case "进群通知":
            return NoticeType.进群通知


async def get_didi_msg(bot: Bot, event: GroupMessageEvent) -> Message:
    """返回要说的话"""
    msg = event.get_message()
    group = await bot.get_group_info(group_id=event.group_id)
    group_name = group["group_name"]
    user_name = event.sender.card if event.sender.card != "" else event.sender.nickname
    msg_header = f"收到 | {user_name}({event.user_id}) | @群【{group_name}】({event.group_id}) | 的滴滴消息\n\n"
    msg[0] = MessageSegment.text(msg_header + str(msg[0])[3:])
    return msg


# ----------------------------------------------------------------
#  matcher实现
# ----------------------------------------------------------------


@bind_server.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_value)):
    """绑定服务器"""
    logger.info(f"<y>群管理</y> | <g>群{event.group_id}</g> | 请求绑定服务器 | {name}")
    response = await api.app_server(name=name)
    if response.code != 200:
        await bind_server.finish(f"绑定失败，未找到服务器：{name}")
    server = response.data["server"]
    await GroupInfo.bind_server(group_id=event.group_id, server=server)
    await bind_server.finish(f"绑定服务器【{server}】成功！")


@set_activity.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_value)):
    """设置活跃值"""
    logger.info(f"<y>群管理</y> | <g>群{event.group_id}</g> | 设置活跃值 | {name}")
    activity = int(name)
    await GroupInfo.set_activity(group_id=event.group_id, activity=activity)
    await set_activity.finish(f"机器人当前活跃值为：{name}")


@robot_status.handle()
async def _(event: GroupMessageEvent, status: bool = Depends(get_status)):
    """设置机器人开关"""
    logger.info(f"<y>群管理</y> | <g>群{event.group_id}</g> | 设置机器人开关 | {status}")
    await GroupInfo.set_status(group_id=event.group_id, status=status)
    name = "开启" if status else "关闭"
    await robot_status.finish(f"设置成功，机器人当前状态为：{name}")


@notice.handle()
async def _(
    event: GroupMessageEvent, notice_type: NoticeType = Depends(get_notice_type)
):
    """设置通知内容"""
    logger.info(
        f"<y>群管理</y> | <g>群{event.group_id}</g> | 设置通知内容 | {notice_type} | {event.get_message()}"
    )
    await source.handle_data_notice(event.group_id, notice_type, event.get_message())
    await notice.finish(f"设置{notice_type.name}成功！")


@meau.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """菜单"""
    pagename = "菜单.html"
    meau_data = await source.get_meau_data(event.group_id)
    nickname = list(bot.config.nickname)[0]
    bot_id = bot.self_id

    img = await browser.template_to_image(
        pagename=pagename, data=meau_data, nickname=nickname, bot_id=bot_id
    )
    await meau.finish(MessageSegment.image(img))


@admin_help.handle()
async def _():
    """管理员帮助"""
    pagename = "管理员帮助.html"
    img = await browser.template_to_image(pagename=pagename)
    await admin_help.finish(MessageSegment.image(img))


@didi.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = Depends(get_didi_msg)):
    """滴滴功能"""
    logger.info(f"<y>群管理</y> | <g>群{event.group_id}</g> | 滴滴功能 | {msg}")
    superusers = list(bot.config.superusers)
    if not superusers:
        await didi.finish("本机器人没有管理员，不知道发给谁呀。")
    for user in superusers:
        await bot.send_private_msg(user_id=int(user), message=msg)
    await didi.finish()


@get_notice.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    """群成员增加事件"""
    # 判断是否为自己
    group_id = event.group_id
    if event.self_id == event.user_id:
        # 机器人被邀请进群，注册消息
        group = await bot.get_group_info(group_id=group_id)
        group_name = group["group_name"]
        logger.info(
            f"加入群【<g>{group_name}</g>】({str(group_id)}) | 操作者：<y>{str(event.operator_id)}</y>"
        )
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

        # 给管理员发送消息
        superusers = list(bot.config.superusers)
        msg = f"我加入了群【{group_name}】({str(group_id)})！"
        for user in superusers:
            try:
                await bot.send_private_msg(user_id=int(user), message=msg)
            except Exception:
                pass

        # 发送欢迎语
        msg = None
        robot_status = await GroupInfo.get_bot_status(group_id=group_id)
        if robot_status:
            nickname = list(bot.config.nickname)[0]
            msg = f"{nickname}驾到，有什么问题来问我吧！"
        await get_notice.finish(msg)

    # 有人进群，发送欢迎语
    flag = await GroupInfo.get_config_status(group_id, GroupSetting.进群通知)
    robot_status = await GroupInfo.get_bot_status(group_id=group_id)
    msg = None
    if flag and robot_status:
        msg = await source.message_decoder(group_id, NoticeType.进群通知)
    await get_notice.finish(msg)


@get_notice.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    """有人离群事件"""
    # 判断是否为自己
    group_id = event.group_id
    if event.self_id == event.user_id:
        # 注销数据
        await source.bot_group_quit(group_id)

        # 给管理员发送消息
        superusers = list(bot.config.superusers)
        for user in superusers:
            try:
                group = await bot.get_group_info(group_id=group_id)
                group_name = group["group_name"]
                logger.info(
                    f"退出群【<g>{group_name}</g>】({str(group_id)}) | 操作者：<y>{str(event.operator_id)}</y>"
                )
                msg = f"我退出了群【{group_name}】({str(group_id)})！"
                await bot.send_private_msg(user_id=int(user), message=msg)
            except Exception:
                pass
        await get_notice.finish()

    # 有人退群，发送退群消息
    flag = await GroupInfo.get_config_status(group_id, GroupSetting.离群通知)
    robot_status = await GroupInfo.get_bot_status(group_id=group_id)
    msg = None
    if flag and robot_status:
        msg = await source.message_decoder(group_id, NoticeType.离群通知)
    await get_notice.finish(msg)


@get_notice.handle()
async def _(bot: Bot, event: FriendAddNoticeEvent):
    """好友增加通知事件"""
    friend = await bot.get_stranger_info(user_id=event.user_id)
    nickname = friend["nickname"]
    msg = f"我添加了好友【{nickname}】({event.user_id})"
    superusers = list(bot.config.superusers)
    async for user_id in GroupList_Async(superusers):
        try:
            await bot.send_private_msg(user_id=user_id, message=msg)
        except Exception:
            pass
    await get_notice.finish()


@get_notice.handle()
async def _(bot: Bot, event: PokeNotifyEvent):
    """群内戳一戳提醒"""
    data = await UserInfo.get_user_data(event.user_id, event.group_id)
    if data["sign"]:
        msg = f"\n今日已签到，\n运势：{data['lucky']}"
    else:
        msg = "\n今日未签到"
    msg += f"\n好感度：{data['friendly']}\n剩余金币：{data['gold']}"
    await get_notice.finish(MessageSegment.at(event.user_id) + msg)


# -------------------------------------------------------------
#   定时功能实现
# -------------------------------------------------------------
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    """晚安通知"""
    logger.info("<y>群管理</y> | 晚安通知 | 正在发送晚安通知")
    all_bot = get_bots()
    for _, bot in all_bot.items():
        group_list: list[dict] = await bot.get_group_list()
        count_all = len(group_list)
        count_success = 0
        count_failed = 0
        count_closed = 0
        time_start = time.time()
        async for group_id in GroupList_Async(group_list):
            goodnight_status = await GroupInfo.get_config_status(
                group_id, GroupSetting.晚安通知
            )
            robot_status = await GroupInfo.get_bot_status(group_id=group_id)
            if goodnight_status and robot_status:
                try:
                    msg = await source.message_decoder(group_id, NoticeType.晚安通知)
                    await bot.send_group_msg(group_id=group_id, message=msg)
                    await asyncio.sleep(random.uniform(0.3, 0.5))
                    count_success += 1
                except Exception:
                    log = f"群({group_id}) | 被禁言了，无法发送晚安..."
                    logger.warning(log)
                    count_failed += 1
            else:
                count_closed += 1
        time_end = time.time()
        time_use = round(time_end - time_start, 2)
        superusers = list(bot.config.superusers)
        for user in superusers:
            msg = f"发送晚安完毕，共发送 {count_all} 个群\n发送成功 {count_success} 个\n发送失败 {count_failed} 个\n关闭通知 {count_closed}个\n用时 {time_use} 秒"
            await bot.send_private_msg(user_id=int(user), message=msg)
