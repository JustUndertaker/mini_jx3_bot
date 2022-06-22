from src.modules.group_info import GroupInfo
from src.modules.user_info import UserInfo

from . import _jx3_event as Event


async def group_init(group_id: int, group_name: str):
    '''注册群数据'''
    await GroupInfo.group_init(group_id, group_name)


async def user_init(user_id: int, group_id: int, user_name: str):
    '''用户注册'''
    await UserInfo.user_init(user_id, group_id, user_name)


async def get_server(group_id: int) -> str:
    '''获取绑定服务器'''
    return await GroupInfo.get_server(group_id)


async def get_ws_status(group_id: int,
                        event: Event.RecvEvent
                        ) -> bool:
    '''
    :说明
        获取ws通知开关，robot为关闭时返回False

    :参数
        * group_id：QQ群号
        * event：接收事件

    :返回
        * bool：ws通知开关
    '''

    bot_status = await GroupInfo.get_bot_status(group_id)
    if not bot_status:
        return False

    if isinstance(event, Event.ServerStatusEvent):
        recv_type = "server"
    if isinstance(event, Event.NewsRecvEvent):
        recv_type = "news"
    if isinstance(event, Event.SerendipityEvent):
        recv_type = "serendipity"
    if isinstance(event, Event.HorseRefreshEvent) or isinstance(event, Event.HorseCatchedEvent):
        recv_type = "horse"
    if isinstance(event, Event.FuyaoRefreshEvent) or isinstance(event, Event.FuyaoNamedEvent):
        recv_type = "fuyao"

    return await GroupInfo.get_ws_status(group_id, recv_type)
