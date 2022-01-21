import asyncio
import random
import time

from nonebot import on_regex, on_request
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.adapters.onebot.v11.event import (FriendRequestEvent,
                                               GroupRequestEvent,
                                               PrivateMessageEvent)
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from src.utils.browser import browser
from src.utils.config import config
from src.utils.utils import GroupList_Async

from . import data_source as source

'''
超级用户插件，实现：
* ticket管理
* 好友管理
* 群管理
* 超级用户帮助
* 管理员广播
'''

# ----------------------------------------------------------------------------
#  macher列表
# ----------------------------------------------------------------------------
get_request = on_request(priority=3, block=True)  # 请求事件
ticket = on_regex(pattern=r"^ticket$", permission=SUPERUSER, priority=2, block=True)  # ticket管理器
friend_list = on_regex(pattern=r"^好友列表$", permission=SUPERUSER, priority=3, block=True)  # 好友列表
friend_delete = on_regex(pattern=r"^删除好友 [\d]+$", permission=SUPERUSER, priority=3, block=True)  # 删除好友
group_list = on_regex(pattern=r"^群列表$", permission=SUPERUSER, priority=3, block=True)  # 群列表
group_delete = on_regex(pattern=r"^退群 [\d]+$", permission=SUPERUSER, priority=3, block=True)  # 退群
borodcast = on_regex(pattern=r"^广播 [\d]+ ", permission=SUPERUSER, priority=3, block=True)  # 广播
borodcast_all = on_regex(pattern=r"^全体广播 ", permission=SUPERUSER, priority=3, block=True)  # 全体广播
handle_robot = on_regex(pattern=r"^(打开|关闭) [0-9]+$", permission=SUPERUSER, priority=3, block=True)  # 打开关闭机器人
help = on_regex(pattern=r"^帮助$", permission=SUPERUSER, priority=3, block=False)  # 帮助
# ----------------------------------------------------------------------------
#  Depends依赖
# ----------------------------------------------------------------------------


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


def get_name(event: PrivateMessageEvent) -> int:
    '''获取后置name'''
    return int(event.get_plaintext().split(" ")[-1])


def get_status(event: PrivateMessageEvent) -> bool:
    '''解析开关'''
    _status = event.get_plaintext()[:2]
    return (_status == "打开")

# ----------------------------------------------------------------------------
#  Macher实现
# ----------------------------------------------------------------------------


@get_request.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    '''好友请求事件'''
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
    flag: bool = config.default['access_group']
    if flag:
        await event.approve(bot)
    else:
        await event.reject(bot)
    await get_request.finish()


@friend_list.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    '''好友列表'''
    user_list = await bot.get_friend_list()
    num = len(user_list)
    pagename = "friend_list.html"
    img = await browser.template_to_image(pagename=pagename, num=num, user_list=user_list)
    await friend_list.finish(MessageSegment.image(img))


@friend_delete.handle()
async def _(bot: Bot, user_id: int = Depends(get_name)):
    '''删除好友'''
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
    _group = await source.get_group_list()
    num = len(_group)
    pagename = "group_list.html"
    img = await browser.template_to_image(pagename=pagename, num=num, group_list=_group)
    await group_list.finish(MessageSegment.image(img))


@group_delete.handle()
async def _(bot: Bot, group_id: int = Depends(get_name)):
    '''退群'''
    flag, group_name = await source.get_group(group_id)
    if flag:
        await bot.set_group_leave(group_id=group_id, is_dismiss=True)
        msg = f"退出群【{group_name}】({group_id})。"
    else:
        msg = f"未找到群：{group_id}"
    await group_delete.finish(msg)


@borodcast.handle()
async def _(bot: Bot, group_id: int = Depends(get_borod_group), message: Message = Depends(get_borod_msg)):
    '''广播消息'''
    msg = None
    try:
        await bot.send_group_msg(group_id=group_id, message=message)
    except Exception as e:
        msg = f"发送失败：{str(e)}"
    await borodcast.finish(msg)


@borodcast_all.handle()
async def _(bot: Bot, message: Message = Depends(get_borod_msg_all)):
    '''广播全体消息'''
    success = 0
    failed = 0
    group_list = await bot.get_group_list()
    start = time.time()
    num = len(group_list)
    async for group_id in GroupList_Async(group_list):
        try:
            await bot.send_group_msg(group_id=group_id, message=message)
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(random.uniform(0.3, 0.5))
    end = time.time()
    use = round(end-start, 2)
    msg = f"广播发送完毕，共发送{num}个群\n成功 {success}个\n失败 {success}个\n共用时 {use}秒。"
    await borodcast_all.finish(msg)


@handle_robot.handle()
async def _(bot: Bot, group_id: int = Depends(get_name), status: bool = Depends(get_status)):
    '''打开关闭机器人'''
    flag, _ = await source.get_group(group_id)
    if flag:
        await source.set_bot_status(group_id, status)
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
