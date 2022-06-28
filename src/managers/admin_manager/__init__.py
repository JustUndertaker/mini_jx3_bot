import asyncio
import random
import time

from nonebot import on_regex, on_request
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.adapters.onebot.v11.event import (FriendRequestEvent,
                                               GroupRequestEvent,
                                               PrivateMessageEvent)
from nonebot.consts import REGEX_DICT
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from nonebot.typing import T_State
from src.modules.group_info import GroupInfo
from src.modules.ticket_info import TicketInfo
from src.params import PluginConfig, jx3api
from src.utils.browser import browser
from src.utils.config import Config
from src.utils.log import logger
from src.utils.utils import GroupList_Async

__plugin_meta__ = PluginMetadata(
    name="超级用户管理",
    description="用于各种superusers的指令",
    usage="超级用户私聊：帮助",
    config=PluginConfig(enable_managed=False)
)

config = Config()

# ----------------------------------------------------------------------------
#   rule检查，检测到私聊消息才会触发
# ----------------------------------------------------------------------------


async def _event_check(event: Event) -> bool:
    return isinstance(event, PrivateMessageEvent)


def CheckEvent() -> bool:
    return Depends(_event_check)


class EventRule:
    async def __call__(self, check: bool = CheckEvent()) -> bool:
        return check


def check_event() -> Rule:
    return Rule(EventRule())


# ----------------------------------------------------------------------------
#  macher列表
# ----------------------------------------------------------------------------
get_request = on_request(priority=3, block=True)  # 请求事件
# ticket管理器
ticket = on_regex(pattern=r"^ticket$", rule=check_event(), permission=SUPERUSER, priority=2, block=True)
# 好友列表
friend_list = on_regex(pattern=r"^好友列表$", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 删除好友
friend_delete = on_regex(pattern=r"^删除好友 (?p<value>[\d]+)$",
                         rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 群列表
group_list = on_regex(pattern=r"^群列表$", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 退群
group_delete = on_regex(pattern=r"^退群 (?p<value>[\d]+)$",
                        rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 广播
borodcast = on_regex(pattern=r"^广播 (?p<value>[\d]+) ", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 全体广播
borodcast_all = on_regex(pattern=r"^全体广播 ", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 打开关闭机器人
handle_robot = on_regex(
    pattern=r"^(?p<command>打开|关闭) (?p<value>[0-9]+)$", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 帮助
help = on_regex(pattern=r"^帮助$", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# 添加ticket
ticket_add = on_regex(pattern=r"^添加 (?p<value>[^\s]+)$", rule=check_event(),
                      permission=SUPERUSER, priority=3, block=True)
# 删除ticket
ticket_del = on_regex(pattern=r"^删除 (?p<value>[\d]+)$", rule=check_event(),
                      permission=SUPERUSER, priority=3, block=True)
# 清理ticket
ticket_clean = on_regex(pattern=r"^清理$", rule=check_event(), permission=SUPERUSER, priority=3, block=True)
# ----------------------------------------------------------------------------
#  Depends依赖
# ----------------------------------------------------------------------------


def get_value(state: T_State) -> str:
    '''
    说明:
        Dependcey，获取命令中的value值

    返回:
        * `value` ：value值
    '''
    regex_dict: dict = state[REGEX_DICT]
    return regex_dict['value']


def get_status(state: T_State) -> bool:
    '''
    说明:
        Dependcey，获取命令中的开关状态

    返回:
        * `bool`：开关状态
    '''
    regex_dict: dict = state[REGEX_DICT]
    return regex_dict['command'] == "打开"


def get_borod_group(event: PrivateMessageEvent) -> int:
    '''获取广播的群号'''
    return int(event.get_plaintext().split(" ")[1])


def get_borod_msg(event: PrivateMessageEvent) -> Message:
    '''获取广播消息'''
    msg = event.get_message()
    msg0 = " ".join(str(msg[0]).split(" ")[2:])
    msg[0] = MessageSegment.text(msg0)
    return msg


def get_borod_msg_all(event: PrivateMessageEvent) -> Message:
    '''获取全体广播信息'''
    msg = event.get_message()
    msg0 = " ".join(str(msg[0]).split(" ")[1:])
    msg[0] = MessageSegment.text(msg0)
    return msg


# ----------------------------------------------------------------------------
#  Macher实现
# ----------------------------------------------------------------------------


@get_request.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    '''好友请求事件'''
    logger.info(
        f"<g>超级用户管理</g> | 收到好友请求：{event.user_id}"
    )
    flag: bool = config.default['access_firend']
    if flag:
        # 接受请求
        await event.approve(bot)
    else:
        await event.reject(bot)
    await get_request.finish()


@get_request.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    '''群请求事件'''
    logger.info(
        f"<g>超级用户管理</g> | 收到群邀请：{event.group_id}"
    )
    flag: bool = config.default['access_group']
    if flag:
        await event.approve(bot)
    else:
        await event.reject(bot)
    await get_request.finish()


@friend_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''好友列表'''
    logger.info(
        f"<g>超级用户管理</g> | {event.user_id} | 请求好友列表"
    )
    user_list = await bot.get_friend_list()
    num = len(user_list)
    pagename = "friend_list.html"
    img = await browser.template_to_image(pagename=pagename, num=num, user_list=user_list)
    await friend_list.finish(MessageSegment.image(img))


@friend_delete.handle()
async def _(bot: Bot, user_id: int = Depends(get_value)):
    '''删除好友'''
    logger.info(
        f"<g>超级用户管理</g> | 请求删除好友：{user_id}"
    )
    user_list = await bot.get_friend_list()
    flag = False
    user_name = ""
    for user in user_list:
        if user_id == user['user_id']:
            flag = True
            user_name = user['nickname']
            break
    if flag:
        bot.call_api(api="delete_friend", id=user_id)
        msg = f'成功，删除好友：{user_name}({user_id})。'
    else:
        msg = f"失败，未找到好友：{user_id}"
    await friend_delete(msg)


@group_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''群列表'''
    logger.info(
        f"<g>超级用户管理</g> | {event.user_id} | 请求群列表"
    )
    group_list = await GroupInfo.get_group_list()
    pagename = "group_list.html"
    img = await browser.template_to_image(pagename=pagename, num=len(group_list), group_list=group_list)
    await group_list.finish(MessageSegment.image(img))


@group_delete.handle()
async def _(bot: Bot, group_id: int = Depends(get_value)):
    '''退群'''
    logger.info(
        f"<g>超级用户管理</g> | 请求退群：{group_id}"
    )
    group_name = await GroupInfo.get_group_name(group_id)
    if group_name:
        await bot.set_group_leave(group_id=group_id, is_dismiss=True)
        msg = f"退出群【{group_name}】({group_id})。"
    else:
        msg = f"未找到群：{group_id}"
    await group_delete.finish(msg)


@borodcast.handle()
async def _(bot: Bot, group_id: int = Depends(get_borod_group), message: Message = Depends(get_borod_msg)):
    '''广播消息'''
    logger.info(
        f"<g>超级用户管理</g> | 广播消息 | {group_id} | {message}"
    )
    msg = None
    try:
        await bot.send_group_msg(group_id=group_id, message=message)
    except Exception as e:
        msg = f"发送失败：{str(e)}"
    await borodcast.finish(msg)


@borodcast_all.handle()
async def _(bot: Bot, message: Message = Depends(get_borod_msg_all)):
    '''广播全体消息'''
    logger.info(
        f"<g>超级用户管理</g> | 全体广播 | {message}"
    )
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
    use = round(end-start, 2)
    msg = f"广播发送完毕，共发送{len(group_list)}个群\n成功 {success}个\n失败 {success}个\n共用时 {use}秒。"
    await borodcast_all.finish(msg)


@handle_robot.handle()
async def _(group_id: int = Depends(get_value), status: bool = Depends(get_status)):
    '''打开关闭机器人'''
    logger.info(
        f"<g>超级用户管理</g> | 打开关闭机器人 | {group_id} | {status}"
    )
    flag = await GroupInfo.get_group_name(group_id)
    if flag:
        await GroupInfo.set_status(group_id, status)
        msg = "设置成功！"
    else:
        msg = f"设置失败，未找到群：{group_id}"
    await handle_robot(msg)


@help.handle()
async def _(event: PrivateMessageEvent):
    '''请求帮助'''
    pagename = "super_help.html"
    img = await browser.template_to_image(pagename=pagename)
    await help.finish(MessageSegment.image(img))


@ticket.handle()
async def _(event: PrivateMessageEvent):
    '''ticket管理器'''
    # 获取ticket列表
    logger.info(
        "<g>超级用户管理</g> | 请求ticket表"
    )
    ticket_list = await TicketInfo.get_all()
    pagename = "ticket.html"
    img = await browser.template_to_image(pagename=pagename, ticket_list=ticket_list)
    await ticket.send(MessageSegment.image(img))


@ticket_add.handle()
async def _(event: PrivateMessageEvent, ticket: str = Depends(get_value)):
    '''添加ticket'''
    logger.info(
        f"<g>超级用户管理</g> | 请求添加ticket | {ticket}"
    )

    response = await jx3api.token_ticket(ticket=ticket)
    if response.code == 200:
        await TicketInfo.append_ticket(ticket)
        msg = "添加ticket成功！"
    else:
        msg = f"添加ticket失败，{response.msg}"

    await ticket_add.finish(msg)


@ticket_del.handle()
async def _(event: PrivateMessageEvent, index: str = Depends(get_value)):
    '''删除ticket'''
    logger.info(
        f"<g>超级用户管理</g> | 请求删除ticket | index:{index}"
    )
    id = int(index)
    flag = await TicketInfo.del_ticket(id)
    if flag:
        msg = "删除ticket成功！"
    else:
        msg = f"删除ticket失败，未找到ticket编号：{index}"
    await ticket_del.finish(msg)


@ticket_clean.handle()
async def _(event: PrivateMessageEvent):
    '''清理ticket'''
    logger.info(
        "<g>超级用户管理</g> | 清理ticket"
    )
    await TicketInfo.clean_ticket()
    await ticket_clean.finish("ticket清理完毕。")
