from nonebot import export, on_regex
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.params import Depends

from . import data_source as source
from .config import DAILIY_LIST

Export = export()
Export.plugin_name = "剑三查询"
Export.plugin_command = "参考“帮助”"
Export.plugin_usage = "剑三游戏查询，数据源使用jx3api"
Export.default_status = True

# ----------------------------------------------------------------
#   正则字典，与jx3api.com的接口对应
# ----------------------------------------------------------------

Regex = {
    "日常查询": r"(^日常$)|(^日常 [\u4e00-\u9fa5]+$)",
    "开服查询": r"(^开服$)|(^开服 [\u4e00-\u9fa5]+$)",
    "金价查询": r"(^金价$)|(^金价 [\u4e00-\u9fa5]+$)",
    "奇穴查询": r"(^奇穴 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+奇穴$)",
    "小药查询": r"(^小药 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+小药$)",
    "配装查询": r"(^配装 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+配装$)",
    "宏查询": r"(^宏 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+宏$)",
    "前置查询": r"^((前置)|(条件)) [\u4e00-\u9fa5]+$",
    "攻略查询": r"(^攻略 [\u4e00-\u9fa5]+$)|(^[\u4e00-\u9fa5]+攻略$)",
    "更新公告": r"(^更新$)|(^公告$)|(^更新公告$)",
    "物价查询": r"^物价 [\u4e00-\u9fa5]+$",
    "奇遇查询": r"(^查询 [(\u4e00-\u9fa5)|(@)]+$)|(^查询 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)",
    "奇遇列表": r"(^奇遇 [\u4e00-\u9fa5]+$)|(^奇遇 [\u4e00-\u9fa5]+ [\u4e00-\u9fa5]+$)",
    "骚话": r"^骚话$",
    "资历排行": r"(^资历排行 [\u4e00-\u9fa5]+$)|(^资历排行 [\u4e00-\u9fa5]+ [\u4e00-\u9fa5]+$)",
    "战绩查询": r"(^战绩 [(\u4e00-\u9fa5)|(@)]+$)|(^战绩 [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)",
    "装备查询": r"(^((装备)|(属性)) [(\u4e00-\u9fa5)|(@)]+$)|(^((装备)|(属性)) [\u4e00-\u9fa5]+ [(\u4e00-\u9fa5)|(@)]+$)",
    "名剑排行": r"(^名剑排行 [0-9]+$)|(^名剑排行$)",
}
'''查询正则字典'''

# ----------------------------------------------------------------
#   matcher列表，定义查询的mathcer
# ----------------------------------------------------------------
daily_query = on_regex(pattern=Regex['日常查询'], permission=GROUP, priority=5, block=True)
server_query = on_regex(pattern=Regex['开服查询'], permission=GROUP, priority=5, block=True)
glod_query = on_regex(pattern=Regex['金价查询'], permission=GROUP, priority=5, block=True)
qixue_query = on_regex(pattern=Regex['奇穴查询'], permission=GROUP, priority=5, block=True)
medicine_query = on_regex(pattern=Regex['小药查询'], permission=GROUP, priority=5, block=True)
equip_group_query = on_regex(pattern=Regex['配装查询'], permission=GROUP, priority=5, block=True)
macro_query = on_regex(pattern=Regex['宏查询'], permission=GROUP, priority=5, block=True)
condition_query = on_regex(pattern=Regex['前置查询'], permission=GROUP, priority=5, block=True)
update_query = on_regex(pattern=Regex['更新公告'], permission=GROUP, priority=5, block=True)
price_query = on_regex(pattern=Regex['物价查询'], permission=GROUP, priority=5, block=True)
serendipity_query = on_regex(pattern=Regex['奇遇查询'], permission=GROUP, priority=5, block=True)
serendipity_list_query = on_regex(pattern=Regex['奇遇列表'], permission=GROUP, priority=5, block=True)
saohua_query = on_regex(pattern=Regex['骚话'], permission=GROUP, priority=5, block=True)
zili_query = on_regex(pattern=Regex['资历排行'], permission=GROUP, priority=5, block=True)
match_query = on_regex(pattern=Regex['战绩查询'], permission=GROUP, priority=5, block=True)
equip_query = on_regex(pattern=Regex['装备查询'], permission=GROUP, priority=5, block=True)
rank_query = on_regex(pattern=Regex['名剑排行'], permission=GROUP, priority=5, block=True)
# ----------------------------------------------------------------
#   Depends函数，用来获取相关参数
# ----------------------------------------------------------------


async def get_server(matcher: Matcher, event: GroupMessageEvent) -> str:
    '''通过depend获取服务器'''
    text_list = event.get_plaintext().split(" ")
    if len(text_list) == 1:
        server = await source.get_server(event.group_id)
    else:
        get_server = text_list[1]
        server = await source.get_main_server(get_server)
        if not server:
            msg = f"未找到服务器[{get_server}]，请验证后查询。"
            await matcher.finish(msg)
    return server


def get_name(event: GroupMessageEvent) -> str:
    '''获取消息中的name字段，取最后分页'''
    return event.get_plaintext().split(" ")[-1]


# ----------------------------------------------------------------
#   handler列表，具体实现回复内容
# ----------------------------------------------------------------


@daily_query.handle()
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    '''日常查询'''
    params = {
        "server": server
    }
    msg, data = await source.get_data_from_api(group_id=event.group_id, app_name="日常查询", params=params)
    if msg != "success":
        msg = f"查询失败，{msg}"
        await daily_query.finish(msg)

    msg = f'日常[{server}]\n'
    msg += f'当前时间：{data.get("date")} 星期{data.get("week")}\n'
    msg += f'今日大战：{data.get("dayWar")}\n'
    msg += f'今日战场：{data.get("dayBattle")}\n'
    msg += f'公共任务：{data.get("dayPublic")}\n'
    msg += f'阵营任务：{data.get("dayCamp")}\n'
    msg += DAILIY_LIST.get(data.get("week"))
    if data.get("dayDraw") is not None:
        msg += f'美人画像：{data.get("dayDraw")}\n'
    msg += f'\n武林通鉴·公共任务\n{data.get("weekPublic")}\n'
    msg += f'武林通鉴·秘境任务\n{data.get("weekFive")}\n'
    msg += f'武林通鉴·团队秘境\n{data.get("weekTeam")}'
    await daily_query.finish(msg)
