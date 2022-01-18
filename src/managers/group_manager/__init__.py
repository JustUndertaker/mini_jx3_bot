from typing import Literal

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.adapters.onebot.v11.event import (GroupDecreaseNoticeEvent,
                                               GroupIncreaseNoticeEvent,
                                               GroupMessageEvent)
from nonebot.adapters.onebot.v11.permission import (GROUP, GROUP_ADMIN,
                                                    GROUP_OWNER)
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from src.utils.browser import browser
from src.utils.log import logger
from src.utils.scheduler import scheduler

from . import data_source as source

'''
群管理插件，实现功能有：
* 绑定服务器
* 设置活跃值
* 机器人开关
* 晚安通知，进群通知，离群通知
* 菜单
* 管理员帮助
* 滴滴
'''
bind_server = on_regex(pattern=r"^绑定 [\u4e00-\u9fa5]+$", permission=SUPERUSER |
                       GROUP_ADMIN | GROUP_OWNER, priority=2, block=True)   # 绑定服务器

set_activity = on_regex(pattern=r"^活跃值 (\d){1,2}$", permission=SUPERUSER |
                        GROUP_ADMIN | GROUP_OWNER, priority=2, block=True)  # 设置活跃值[0-99]

robot_status = on_regex(pattern=r"^机器人 [开关]$", permission=SUPERUSER |
                        GROUP_ADMIN | GROUP_OWNER, priority=2, block=True)  # 设置机器人开关

notice = on_regex(pattern=r"^((晚安)|(离群)|(进群))通知 ", permission=SUPERUSER |
                  GROUP_ADMIN | GROUP_OWNER, priority=2, block=True)    # 晚安通知，离群通知，进群通知

meau = on_regex(pattern=r"^((菜单)|(状态))$", permission=GROUP,  priority=3, block=True)  # 菜单

admin_help = on_regex(pattern=r"^管理员帮助$", permission=GROUP, priority=3, block=True)  # 管理员帮助

didi = on_regex(pattern=r"^滴滴 ", permission=GROUP_ADMIN | GROUP_OWNER, priority=3, block=True)  # 滴滴


# -------------------------------------------------------------
#   Depends依赖
# -------------------------------------------------------------
def get_name(event: GroupMessageEvent) -> str:
    '''获取后置文本内容'''
    return event.get_plaintext().split(" ")[-1]


def get_status(event: GroupMessageEvent) -> bool:
    '''获取机器人开关'''
    status = event.get_plaintext().split(" ")[-1]
    return status == "开"


def get_notice_type(event: GroupMessageEvent) -> Literal["晚安通知", "离群通知", "进群通知"]:
    '''返回通知类型'''
    return event.get_plaintext()[:4]


# ----------------------------------------------------------------
#  matcher实现
# ----------------------------------------------------------------
@bind_server.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_name)):
    '''绑定服务器'''
    server = await source.get_main_server(name)
    if server is None:
        await bind_server.finish(f"绑定失败，未找到服务器：{name}")

    await source.bind_server(event.group_id, server)
    await bind_server.finish(f"绑定服务器【{server}】成功！")


@set_activity.handle()
async def _(event: GroupMessageEvent, name: str = Depends(get_name)):
    '''设置活跃值'''
    activity = int(name)
    await source.set_activity(event.group_id, activity)
    await set_activity.finish(f"机器人当前活跃值为：{name}")


@robot_status.handle()
async def _(event: GroupMessageEvent, status: bool = Depends(get_status)):
    '''设置机器人开关'''
    await source.set_status(event.group_id, status)
    name = "开启"if status else "关闭"
    await robot_status.finish(f"设置成功，机器人当前状态为：{name}")


@notice.handle()
async def _(event: GroupMessageEvent, notice_type: str = Depends(get_notice_type)):
    '''设置通知内容'''
    pass


@meau.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    '''菜单'''
    pagename = "meau.html"
    meau_data = await source.get_meau_data(event.group_id)
    nickname = list(bot.config.nickname)[0]
    bot_id = bot.self_id

    img = await browser.template_to_image(pagename=pagename,
                                          data=meau_data,
                                          nickname=nickname,
                                          bot_id=bot_id
                                          )
    await meau.finish(MessageSegment.image(img))


@admin_help.handle()
async def _():
    '''管理员帮助'''
    pagename = "admin_help.html"
    img = await browser.template_to_image(pagename=pagename)
    await admin_help.finish(MessageSegment.image(img))
