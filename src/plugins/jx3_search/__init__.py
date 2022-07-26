import time
from datetime import datetime
from enum import Enum

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GROUP, GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Depends, RegexDict
from nonebot.plugin import PluginMetadata

from src.internal.jx3api import JX3API
from src.modules.group_info import GroupInfo
from src.modules.search_record import SearchRecord
from src.modules.ticket_info import TicketInfo
from src.params import PluginConfig
from src.utils.browser import browser
from src.utils.log import logger

from . import data_source as source
from .config import DAILIY_LIST, JX3PROFESSION

__plugin_meta__ = PluginMetadata(
    name="剑三查询", description="剑三游戏查询，数据源使用jx3api", usage="参考“帮助”", config=PluginConfig()
)

api = JX3API()
"""jx3api接口实例"""

# ----------------------------------------------------------------
#   正则枚举，已实现的查询功能
# ----------------------------------------------------------------


class REGEX(Enum):
    """正则枚举"""

    日常任务 = r"^日常$|^日常 (?P<server>[\u4e00-\u9fa5]+)$"
    开服检查 = r"^开服$|^开服 (?P<server>[\u4e00-\u9fa5]+)$"
    金价比例 = r"^金价$|^金价 (?P<server>[\u4e00-\u9fa5]+)$"
    推荐小药 = r"^小药 (?P<value1>[\u4e00-\u9fa5]+)$|^(?P<value2>[\u4e00-\u9fa5]+)小药$"
    推荐装备 = r"^配装 (?P<value1>[\u4e00-\u9fa5]+)$|^(?P<value2>[\u4e00-\u9fa5]+)配装$"
    查宏命令 = r"^宏 (?P<value1>[\u4e00-\u9fa5]+)$|^(?P<value2>[\u4e00-\u9fa5]+)宏$"
    阵眼效果 = r"^阵眼 (?P<value1>[\u4e00-\u9fa5]+)$|^(?P<value2>[\u4e00-\u9fa5]+)阵眼$"
    物品价格 = r"^物价 (?P<value1>[\u4e00-\u9fa5]+)$"
    随机骚话 = r"^骚话$"
    奇遇前置 = r"^(?:(?:前置)|(?:条件)) (?P<value1>[\u4e00-\u9fa5]+)$"
    奇遇攻略 = r"^攻略 (?P<value1>[\u4e00-\u9fa5]+)$|^(?P<value2>[\u4e00-\u9fa5]+)攻略$"
    更新公告 = r"^更新$|^公告$|^更新公告$"
    奇遇查询 = r"^查询 (?P<value1>[\S]+)$|^查询 (?P<server>[\u4e00-\u9fa5]+) (?P<value2>[\S]+)$"
    奇遇统计 = r"^奇遇 (?P<value1>[\S]+)$|^奇遇 (?P<server>[\u4e00-\u9fa5]+) (?P<value2>[\S]+)$"
    奇遇汇总 = r"^汇总$|^汇总 (?P<server>[\u4e00-\u9fa5]+)$"
    比赛战绩 = r"^战绩 (?P<value1>[\S]+)$|^战绩 (?P<server>[\u4e00-\u9fa5]+) (?P<value2>[\S]+)$"
    装备属性 = r"^(?:(?:装备)|(?:属性)) (?P<value1>[\S]+)$|^(?:(?:装备)|(?:属性)) (?P<server>[\u4e00-\u9fa5]+) (?P<value2>[\S]+)$"


# ----------------------------------------------------------------
#   matcher列表，定义查询的mathcer
# ----------------------------------------------------------------
daily_query = on_regex(
    pattern=REGEX.日常任务.value, permission=GROUP, priority=5, block=True
)
server_query = on_regex(
    pattern=REGEX.开服检查.value, permission=GROUP, priority=5, block=True
)
gold_query = on_regex(
    pattern=REGEX.金价比例.value, permission=GROUP, priority=5, block=True
)
medicine_query = on_regex(
    pattern=REGEX.推荐小药.value, permission=GROUP, priority=5, block=True
)
equip_group_query = on_regex(
    pattern=REGEX.推荐装备.value, permission=GROUP, priority=5, block=True
)
macro_query = on_regex(
    pattern=REGEX.查宏命令.value, permission=GROUP, priority=5, block=True
)
zhenyan_query = on_regex(
    pattern=REGEX.阵眼效果.value, permission=GROUP, priority=5, block=True
)
condition_query = on_regex(
    pattern=REGEX.奇遇前置.value, permission=GROUP, priority=5, block=True
)
strategy_query = on_regex(
    pattern=REGEX.奇遇攻略.value, permission=GROUP, priority=5, block=True
)
update_query = on_regex(
    pattern=REGEX.更新公告.value, permission=GROUP, priority=5, block=True
)
price_query = on_regex(
    pattern=REGEX.物品价格.value, permission=GROUP, priority=5, block=True
)
serendipity_query = on_regex(
    pattern=REGEX.奇遇查询.value, permission=GROUP, priority=5, block=True
)
serendipity_list_query = on_regex(
    pattern=REGEX.奇遇统计.value, permission=GROUP, priority=5, block=True
)
serendipity_summary_query = on_regex(
    pattern=REGEX.奇遇汇总.value, permission=GROUP, priority=5, block=True
)
saohua_query = on_regex(
    pattern=REGEX.随机骚话.value, permission=GROUP, priority=5, block=True
)
match_query = on_regex(
    pattern=REGEX.比赛战绩.value, permission=GROUP, priority=5, block=True
)
equip_query = on_regex(
    pattern=REGEX.装备属性.value, permission=GROUP, priority=5, block=True
)
help = on_regex(pattern=r"^帮助$", permission=GROUP, priority=5, block=True)


# ----------------------------------------------------------------
#   Dependency，用来获取相关参数及冷却实现
# ----------------------------------------------------------------


async def get_server(
    matcher: Matcher, event: GroupMessageEvent, regex_dict: dict = RegexDict()
) -> str:
    """
    说明:
        Dependency，获取匹配字符串中的server，如果没有则获取群绑定的默认server
    """
    _server = regex_dict.get("server")
    if _server:
        response = await api.app_server(name=_server)
        if response.code != 200:
            msg = f"未找到服务器[{_server}]，请验证后查询。"
            await matcher.finish(msg)
        server: str = response.data["server"]
    else:
        server = await GroupInfo.get_server(event.group_id)
    return server


async def get_value(regex_dict: dict = RegexDict()) -> str:
    """
    说明:
        Dependency，获取匹配字符串中的value字段
    """
    value = regex_dict.get("value1")
    return value if value else regex_dict.get("value2")


async def get_profession(matcher: Matcher, name: str = Depends(get_value)) -> str:
    """
    说明:
        Dependency，通过别名获取职业名称
    """
    profession = JX3PROFESSION.get_profession(name)
    if profession:
        return profession

    # 未找到职业
    msg = f"未找到职业[{name}]，请检查参数。"
    await matcher.finish(msg)


def cold_down(name: str, cd_time: int) -> None:
    """
    说明:
        Dependency，增加命令冷却，同时会在数据库中记录一次查询

    参数:
        * `name`：app名称，相同名称会使用同一组cd
        * `cd_time`：冷却时间

    用法:
    ```
        @matcher.handle(parameterless=[cold_down(name="app", cd_time=0)])
        async def _():
            pass
    ```
    """

    async def dependency(matcher: Matcher, event: GroupMessageEvent):
        time_last = await SearchRecord.get_search_time(event.group_id, name)
        time_now = int(time.time())
        over_time = over_time = time_now - time_last
        if over_time > cd_time:
            await SearchRecord.use_search(event.group_id, name)
            return
        else:
            left_cd = cd_time - over_time
            await matcher.finish(f"[{name}]冷却中 ({left_cd})")

    return Depends(dependency)


# ----------------------------------------------------------------
#   handler列表，具体实现回复内容
# ----------------------------------------------------------------


@daily_query.handle(parameterless=[cold_down(name="日常查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    """日常查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 日常查询 | 请求：{server}"
    )
    response = await api.app_daily(server=server)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await daily_query.finish(msg)

    data = response.data
    msg = (
        f"日常[{server}]\n"
        f'当前时间：{data.get("date","未知")} 星期{data.get("week","未知")}\n'
        f'今日大战：{data.get("war","未知")}\n'
        f'今日战场：{data.get("battle","未知")}\n'
        f'公共任务：{data.get("relief","未知")}\n'
        f'阵营任务：{data.get("camp","未知")}\n'
        f'阵营任务：{data.get("camp","未知")}\n'
        f'{DAILIY_LIST.get(data.get("week", "未知"))}'
    )
    if data.get("draw"):
        msg += f'美人画像：{data.get("draw")}\n'
    team: list = data.get("team")
    msg += f"\n武林通鉴·公共任务\n{team[0]}\n" f"武林通鉴·秘境任务\n{team[1]}\n" f"武林通鉴·团队秘境\n{team[2]}"
    await daily_query.finish(msg)


@server_query.handle(parameterless=[cold_down(name="开服查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    """开服查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 开服查询 | 请求：{server}"
    )
    response = await api.app_check(server=server)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await server_query.finish(msg)

    data = response.data
    status = "已开服" if data["status"] == 1 else "维护中"
    msg = f"{server} 当前状态是[{status}]"
    await server_query.finish(msg)


@gold_query.handle(parameterless=[cold_down(name="金价查询", cd_time=0)])
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    """金价查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 金价查询 | 请求：{server}"
    )
    response = await api.app_demon(server=server)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await gold_query.finish(msg)

    data: dict = response.data[0]
    date_now = datetime.now().strftime("%m-%d %H:%M")
    msg = (
        f"金价[{server}] {date_now}\n"
        f'官方平台：1元={data.get("wanbaolou")}金\n'
        f'百度贴吧：1元={data.get("tieba")}金\n'
        f'悠悠平台：1元={data.get("uu898")}金\n'
        f'嘟嘟平台：1元={data.get("dd373")}金\n'
        f'其他平台：1元={data.get("5173")}金'
    )
    await gold_query.finish(msg)


@medicine_query.handle(parameterless=[cold_down(name="小药查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_profession)):
    """小药查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 小药查询 | 请求：{name}")
    response = await api.app_heighten(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await medicine_query.finish(msg)

    data = response.data
    name = data.get("name")
    msg = (
        f"[{name}]小药：\n"
        f'增强食品：{data.get("heighten_food")}\n'
        f'辅助食品：{data.get("auxiliary_food")}\n'
        f'增强药品：{data.get("heighten_drug")}\n'
        f'辅助药品：{data.get("auxiliary_drug")}\n'
    )

    await medicine_query.finish(msg)


@equip_group_query.handle(parameterless=[cold_down(name="配装查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_profession)):
    """配装查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 配装查询 | 请求：{name}")
    response = await api.app_equip(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await equip_group_query.finish(msg)

    data = response.data
    msg = (
        MessageSegment.text(f'{data.get("name")}配装：\nPve装备：\n')
        + MessageSegment.image(data.get("pve"))
        + MessageSegment.text("Pvp装备：\n")
        + MessageSegment.image(data.get("pvp"))
    )
    await equip_group_query.finish(msg)


@macro_query.handle(parameterless=[cold_down(name="宏查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_profession)):
    """宏查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 宏查询 | 请求：{name}")
    response = await api.app_macro(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await macro_query.finish(msg)

    data = response.data
    msg = (
        f'宏 {data.get("name")} 更新时间：{data.get("time")}\n'
        f'{data.get("macro")}\n'
        f'奇穴：{data.get("qixue")}'
    )

    await macro_query.finish(msg)


@zhenyan_query.handle(parameterless=[cold_down(name="阵眼查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_profession)):
    """阵眼查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 阵眼查询 | 请求：{name}")
    response = await api.app_matrix(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await zhenyan_query.finish(msg)

    data = response.data
    msg = f"{name}：【{data.get('skillName')}】\n"
    descs: list[dict] = data.get("descs")
    for i in descs:
        msg += f"{i.get('name')}：{i.get('desc')}\n"
    await zhenyan_query.finish(msg)


@condition_query.handle(parameterless=[cold_down(name="前置查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_value)):
    """前置查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 前置查询 | 请求：{name}")
    response = await api.app_require(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await condition_query.finish(msg)

    data = response.data
    url = data.get("upload")
    msg = MessageSegment.image(url)
    await condition_query.finish(msg)


@strategy_query.handle(parameterless=[cold_down(name="攻略查询", cd_time=0)])
async def _(event: GroupMessageEvent, name: str = Depends(get_value)):
    """攻略查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 攻略查询 | 请求：{name}")
    token = api.config.api_token
    if token != "":
        response = await api.next_strategy(name=name)
    else:
        response = await api.app_strategy(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await strategy_query.finish(msg)

    data = response.data
    img = data["url"]
    await strategy_query.finish(MessageSegment.image(img))


@update_query.handle(parameterless=[cold_down(name="更新公告", cd_time=0)])
async def _(event: GroupMessageEvent):
    """更新公告"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 更新公告查询")
    url = "https://jx3.xoyo.com/launcher/update/latest.html"
    img = await browser.get_image_from_url(url=url, width=130, height=480)
    msg = MessageSegment.image(img)
    log = f"群{event.group_id} | 查询更新公告"
    logger.info(log)
    await update_query.finish(msg)


@saohua_query.handle(parameterless=[cold_down(name="骚话", cd_time=0)])
async def _(event: GroupMessageEvent):
    """骚话"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 骚话 | 请求骚话")
    response = await api.app_random()
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await saohua_query.finish(msg)

    data = response.data
    await saohua_query.finish(data["text"])


# -------------------------------------------------------------
#   下面是使用模板生成的图片事件
# -------------------------------------------------------------


@price_query.handle(parameterless=[cold_down(name="物价查询", cd_time=10)])
async def _(event: GroupMessageEvent, name: str = Depends(get_value)):
    """物价查询"""
    logger.info(f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 物价查询 | 请求：{name}")
    response = await api.app_price(name=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await price_query.finish(msg)

    data = response.data
    pagename = "物品价格.html"
    item_name = data.get("name")
    item_info = data.get("info")
    item_img = data.get("upload")
    item_data = source.handle_data_price(data.get("data"))
    img = await browser.template_to_image(
        pagename=pagename,
        name=item_name,
        info=item_info,
        image=item_img,
        data=item_data,
    )
    await price_query.finish(MessageSegment.image(img))


@serendipity_query.handle(parameterless=[cold_down(name="角色奇遇", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = Depends(get_server),
    name: str = Depends(get_value),
):
    """角色奇遇查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 角色奇遇查询 | 请求：server:{server},name:{name}"
    )

    ticket = await TicketInfo.get_ticket()
    response = await api.next_serendipity(server=server, name=name, ticket=ticket)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_query.finish(msg)

    data = response.data
    pagename = "角色奇遇.html"
    get_data = source.handle_data_serendipity(data)
    img = await browser.template_to_image(
        pagename=pagename, server=server, name=name, data=get_data
    )
    await serendipity_query.finish(MessageSegment.image(img))


@serendipity_list_query.handle(parameterless=[cold_down(name="奇遇统计", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = Depends(get_server),
    name: str = Depends(get_value),
):
    """奇遇统计查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 奇遇统计查询 | 请求：server:{server},serendipity:{name}"
    )
    response = await api.next_statistical(server=server, serendipity=name)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_list_query.finish(msg)

    data = response.data
    pagename = "奇遇统计.html"
    get_data = source.handle_data_serendipity_list(data)
    img = await browser.template_to_image(
        pagename=pagename, server=server, name=name, data=get_data
    )
    await serendipity_list_query.finish(MessageSegment.image(img))


@serendipity_summary_query.handle(parameterless=[cold_down(name="奇遇汇总", cd_time=10)])
async def _(event: GroupMessageEvent, server: str = Depends(get_server)):
    """奇遇汇总查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 奇遇汇总查询 | 请求：{server}"
    )
    response = await api.next_collect(server=server)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await serendipity_summary_query.finish(msg)

    data = response.data
    pagename = "奇遇汇总.html"
    get_data = source.handle_data_serendipity_summary(data)
    img = await browser.template_to_image(
        pagename=pagename, server=server, data=get_data
    )
    await serendipity_summary_query.finish(MessageSegment.image(img))


@match_query.handle(parameterless=[cold_down(name="战绩查询", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = Depends(get_server),
    name: str = Depends(get_value),
):
    """战绩查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 战绩查询 | 请求：server:{server},name:{name}"
    )
    ticket = await TicketInfo.get_ticket()
    response = await api.next_arena(server=server, name=name, ticket=ticket)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await match_query.finish(msg)

    data = response.data
    pagename = "比赛记录.html"
    get_data = source.handle_data_match(data)
    img = await browser.template_to_image(
        pagename=pagename, server=server, name=name, data=get_data
    )
    await match_query.finish(MessageSegment.image(img))


@equip_query.handle(parameterless=[cold_down(name="装备属性", cd_time=10)])
async def _(
    event: GroupMessageEvent,
    server: str = Depends(get_server),
    name: str = Depends(get_value),
):
    """装备属性查询"""
    logger.info(
        f"<y>群{event.group_id}</y> | <g>{event.user_id}</g> | 装备属性查询 | 请求：server:{server},name:{name}"
    )
    ticket = await TicketInfo.get_ticket()
    response = await api.role_attribute(server=server, name=name, ticket=ticket)
    if response.code != 200:
        msg = f"查询失败，{response.msg}"
        await equip_query.finish(msg)

    data = response.data
    pagename = "角色装备.html"
    get_data = source.handle_data_equip(data)
    img = await browser.template_to_image(
        pagename=pagename, server=server, name=name, data=get_data
    )
    await equip_query.finish(MessageSegment.image(img))


@help.handle()
async def _(event: GroupMessageEvent):
    """帮助"""
    token = api.config.api_token
    flag = token != ""
    pagename = "查询帮助.html"
    img = await browser.template_to_image(pagename=pagename, flag=flag)
    await help.finish(MessageSegment.image(img))
