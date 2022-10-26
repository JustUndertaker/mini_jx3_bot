import asyncio
import random
import time

from nonebot import on_request
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendRequestEvent,
    GroupRequestEvent,
    Message,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule

from src.config import default_config
from src.internal.jx3api import JX3API
from src.modules.group_info import GroupInfo
from src.modules.ticket_info import TicketInfo
from src.params import PluginConfig, admin_matcher_group
from src.utils.browser import browser
from src.utils.log import logger
from src.utils.utils import GroupList_Async

__plugin_meta__ = PluginMetadata(
    name="超级用户管理",
    description="用于各种superusers的指令",
    usage="超级用户私聊：帮助",
    config=PluginConfig(enable_managed=False),
)

api = JX3API()
"""jx3api接口实例"""

# ----------------------------------------------------------------------------
#   rule检查，检测到私聊消息才会触发
# ----------------------------------------------------------------------------


def check_event() -> Rule:
    """匹配私聊消息"""

    def check(event: Event) -> bool:
        return isinstance(event, PrivateMessageEvent)

    return Rule(check)


# ----------------------------------------------------------------------------
#  macher列表
# ----------------------------------------------------------------------------
get_request = on_request(priority=3, block=True)  # 请求事件
# ticket管理器
ticket = admin_matcher_group.on_regex(pattern=r"^ticket$")
# 好友列表
friend_list = admin_matcher_group.on_regex(pattern=r"^好友列表$")
# 删除好友
friend_delete = admin_matcher_group.on_regex(pattern=r"^删除好友 (?P<value>[\d]+)$")
# 群列表
group_list = admin_matcher_group.on_regex(pattern=r"^群列表$")
# 退群
group_delete = admin_matcher_group.on_regex(pattern=r"^退群 (?P<value>[\d]+)$")
# 广播
borodcast = admin_matcher_group.on_regex(pattern=r"^广播 (?P<value>[\d]+) ")
# 全体广播
borodcast_all = admin_matcher_group.on_regex(pattern=r"^全体广播 ")
# 打开关闭机器人
handle_robot = admin_matcher_group.on_regex(
    pattern=r"^(?P<command>打开|关闭) (?P<value>[\d]+)$"
)
# 帮助
help = admin_matcher_group.on_regex(pattern=r"^帮助$")
# 添加ticket
ticket_add = admin_matcher_group.on_regex(pattern=r"^添加 (?P<value>[^\s]+)$")
# 删除ticket
ticket_del = admin_matcher_group.on_regex(pattern=r"^删除 (?P<value>[\d]+)$")
# 清理ticket
ticket_clean = admin_matcher_group.on_regex(pattern=r"^清理$")

# ----------------------------------------------------------------------------
#  Depends依赖
# ----------------------------------------------------------------------------


def get_value() -> str:
    """
    说明:
        Dependency，获取命令中的value值

    返回:
        * `value` ：value值
    """

    def dependency(regex_dict: dict = RegexDict()) -> str:
        return regex_dict["value"]

    return Depends(dependency)


def get_status() -> bool:
    """
    说明:
        Dependency，获取命令中的开关状态

    返回:
        * `bool`：开关状态
    """

    def dependency(regex_dict: dict = RegexDict()) -> bool:
        return regex_dict["command"] == "打开"

    return Depends(dependency)


def get_borod_group() -> int:
    """
    说明:
        Dependency，获取广播的群号
    """

    def dependency(regex_dict: dict = RegexDict()) -> int:
        return int(regex_dict["value"])

    return Depends(dependency)


def get_borod_msg() -> Message:
    """
    说明:
        Dependency，获取广播消息
    """

    def dependency(event: PrivateMessageEvent) -> Message:
        msg = event.get_message()
        msg_head = "来自管理员的广播消息：\n\n"
        msg0 = msg_head + " ".join(str(msg[0]).split(" ")[2:])
        msg[0] = MessageSegment.text(msg0)
        return msg

    return Depends(dependency)


def get_borod_msg_all() -> Message:
    """
    说明:
        Dependency，获取全体广播信息
    """

    def dependency(event: PrivateMessageEvent) -> Message:
        msg = event.get_message()
        msg_head = "来自管理员的广播消息：\n\n"
        msg0 = msg_head + " ".join(str(msg[0]).split(" ")[1:])
        msg[0] = MessageSegment.text(msg0)
        return msg

    return Depends(dependency)


# ----------------------------------------------------------------------------
#  Macher实现
# ----------------------------------------------------------------------------


@get_request.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    """好友请求事件"""
    logger.info(f"<g>超级用户管理</g> | 收到好友请求：{event.user_id}")
    if default_config.access_firend:
        # 接受请求
        await event.approve(bot)
    else:
        await event.reject(bot)
    await get_request.finish()


@get_request.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    """群请求事件"""
    logger.info(f"<g>超级用户管理</g> | 收到群邀请：{event.group_id}")
    if default_config.access_group:
        await event.approve(bot)
    else:
        await event.reject(bot)
    await get_request.finish()


@friend_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    """好友列表"""
    logger.info(f"<g>超级用户管理</g> | {event.user_id} | 请求好友列表")
    user_list = await bot.get_friend_list()
    num = len(user_list)
    pagename = "好友列表.html"
    img = await browser.template_to_image(
        pagename=pagename, num=num, user_list=user_list
    )
    await friend_list.finish(MessageSegment.image(img))


@friend_delete.handle()
async def _(bot: Bot, user_id: str = get_value()):
    """删除好友"""
    logger.info(f"<g>超级用户管理</g> | 请求删除好友：{user_id}")
    user_list = await bot.get_friend_list()
    flag = False
    user_name = ""
    for user in user_list:
        if user_id == user["user_id"]:
            flag = True
            user_name = user["nickname"]
            break
    if flag:
        bot.call_api(api="delete_friend", id=user_id)
        msg = f"成功，删除好友：{user_name}({user_id})。"
    else:
        msg = f"失败，未找到好友：{user_id}"
    await friend_delete.finish(msg)


@group_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    """群列表"""
    logger.info(f"<g>超级用户管理</g> | {event.user_id} | 请求群列表")
    get_group_list = await GroupInfo.get_group_list()
    pagename = "群列表.html"
    img = await browser.template_to_image(
        pagename=pagename, num=len(get_group_list), group_list=get_group_list
    )
    await group_list.finish(MessageSegment.image(img))


@group_delete.handle()
async def _(bot: Bot, group_id: str = get_value()):
    """退群"""
    logger.info(f"<g>超级用户管理</g> | 请求退群：{group_id}")
    group_name = await GroupInfo.get_group_name(int(group_id))
    if group_name:
        await bot.set_group_leave(group_id=int(group_id), is_dismiss=True)
        msg = f"退出群【{group_name}】({group_id})。"
    else:
        msg = f"未找到群：{group_id}"
    await group_delete.finish(msg)


@borodcast.handle()
async def _(
    bot: Bot,
    group_id: int = get_borod_group(),
    message: Message = get_borod_msg(),
):
    """广播消息"""
    logger.info(f"<g>超级用户管理</g> | 广播消息 | {group_id} | {message}")
    msg = None
    try:
        await bot.send_group_msg(group_id=group_id, message=message)
        msg = f"广播消息成功，群：{group_id}。"
    except Exception as e:
        msg = f"发送失败：{str(e)}"
    await borodcast.finish(msg)


@borodcast_all.handle()
async def _(bot: Bot, message: Message = get_borod_msg_all()):
    """广播全体消息"""
    logger.info(f"<g>超级用户管理</g> | 全体广播 | {message}")
    success = 0
    failed = 0
    group_list = await GroupInfo.get_group_list()
    start = time.time()
    async for group_id in GroupList_Async(group_list):
        try:
            await bot.send_group_msg(group_id=group_id, message=message)
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(random.uniform(0.3, 0.5))
    end = time.time()
    use = round(end - start, 2)
    msg = f"广播发送完毕，共发送{len(group_list)}个群\n成功 {success}个\n失败 {failed}个\n共用时 {use}秒。"
    await borodcast_all.finish(msg)


@handle_robot.handle()
async def _(group_id: str = get_value(), status: bool = get_status()):
    """打开关闭机器人"""
    logger.info(f"<g>超级用户管理</g> | 打开关闭机器人 | {group_id} | {status}")
    flag = await GroupInfo.get_group_name(int(group_id))
    if flag:
        await GroupInfo.set_status(int(group_id), status)
        msg = "设置成功！"
    else:
        msg = f"设置失败，未找到群：{group_id}"
    await handle_robot.finish(msg)


@help.handle()
async def _(event: PrivateMessageEvent):
    """请求帮助"""
    pagename = "超级用户帮助.html"
    img = await browser.template_to_image(pagename=pagename)
    await help.finish(MessageSegment.image(img))


@ticket.handle()
async def _(event: PrivateMessageEvent):
    """ticket管理器"""
    # 获取ticket列表
    logger.info("<g>超级用户管理</g> | 请求ticket表")
    ticket_list = await TicketInfo.get_all()
    pagename = "ticket.html"
    img = await browser.template_to_image(pagename=pagename, ticket_list=ticket_list)
    await ticket.send(MessageSegment.image(img))


@ticket_add.handle()
async def _(event: PrivateMessageEvent, ticket: str = get_value()):
    """添加ticket"""
    logger.info(f"<g>超级用户管理</g> | 请求添加ticket | {ticket}")

    response = await api.data_token_ticket(ticket=ticket)
    if response.code == 200:
        await TicketInfo.append_ticket(ticket)
        msg = "添加ticket成功！"
    else:
        msg = f"添加ticket失败，{response.msg}"

    await ticket_add.finish(msg)


@ticket_del.handle()
async def _(event: PrivateMessageEvent, index: str = get_value()):
    """删除ticket"""
    logger.info(f"<g>超级用户管理</g> | 请求删除ticket | index:{index}")
    id = int(index)
    flag = await TicketInfo.del_ticket(id)
    if flag:
        msg = "删除ticket成功！"
    else:
        msg = f"删除ticket失败，未找到ticket编号：{index}"
    await ticket_del.finish(msg)


@ticket_clean.handle()
async def _(event: PrivateMessageEvent):
    """清理ticket"""
    logger.info("<g>超级用户管理</g> | 清理ticket")
    await TicketInfo.clean_ticket()
    await ticket_clean.finish("ticket清理完毕。")
