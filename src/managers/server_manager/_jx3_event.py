import time
from datetime import datetime
from typing import List, Optional

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import overrides
from nonebot.utils import escape_tag


class WsClosed(BaseEvent):
    '''ws被关闭事件'''
    __event__ = "WsClosed"
    post_type: str = "WsClosed"
    reason: Optional[str]
    '''关闭原因'''

    def __init__(self, reason: str):
        super().__init__()
        self.reason = reason

    @property
    def log(self) -> str:
        '''事件日志内容'''
        return ""

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class RecvEvent(BaseEvent):
    '''ws推送事件基类'''
    __event__ = "WsRecv"
    post_type: str = "WsRecv"
    message_type: Optional[str]
    server: Optional[str] = None
    '''影响服务器'''

    @property
    def log(self) -> str:
        '''事件日志内容'''
        return ""

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        message_type = getattr(self, "message_type", None)
        return f"{self.post_type}" + (
            f".{message_type}" if message_type else ""
        )

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


class ServerStatusEvent(RecvEvent):
    '''服务器状态推送事件'''
    __event__ = "WsRecv.ServerStatus"
    message_type = "ServerStatus"
    status: Optional[bool]
    '''服务器状态'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        status = data.get('status')
        self.status = (True if status == 1 else False)

    @property
    def log(self) -> str:
        if self.status == 1:
            status = "已开服"
        else:
            status = "已维护"
        log = f"开服推送事件：[{self.server}]状态-{status}"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        time_now = datetime.now().strftime("%H时%M分")
        if self.status:
            return Message(
                f'时间：{time_now}\n[{self.server}] 开服啦！'
            )
        else:
            return Message(
                f'时间{time_now}\n[{self.server}]维护惹。'
            )


class NewsRecvEvent(RecvEvent):
    '''新闻推送事件'''
    __event__ = "WsRecv.News"
    message_type = "News"
    news_type: Optional[str]
    '''新闻类型'''
    news_tittle: Optional[str]
    '''新闻标题'''
    news_url: Optional[str]
    '''新闻url链接'''
    news_date: Optional[str]
    '''新闻日期'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.news_type = data.get('type')
        self.news_tittle = data.get('title')
        self.news_url = data.get('url')
        self.news_date = data.get('date')

    @property
    def log(self) -> str:
        log = f"[{self.news_type}]事件：{self.news_tittle}"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[{self.news_type}]来惹\n标题：{self.news_tittle}\n链接：{self.news_url}\n日期：{self.news_date}"
        )


class SerendipityEvent(RecvEvent):
    '''奇遇推送事件'''
    __event__ = "WsRecv.Serendipity"
    message_type = "Serendipity"
    name: Optional[str]
    '''触发角色'''
    serendipity: Optional[str]
    '''奇遇名'''
    level: Optional[int]
    '''奇遇等级'''
    time: Optional[str]
    '''触发时间'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        self.name = data.get('name')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%m/%d %H:%M', start_trans)
        self.serendipity = data.get('serendipity')
        self.level = data.get('level')

    @property
    def log(self) -> str:
        log = f"奇遇推送事件：[{self.server}]的[{self.name}]抱走了奇遇：{self.serendipity}"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f'奇遇推送 {self.time}\n{self.serendipity} 被 {self.name} 抱走惹。'
        )


class HorseRefreshEvent(RecvEvent):
    '''马驹刷新事件'''
    __event__ = "WsRecv.HorseRefresh"
    message_type = "HorseRefresh"
    map: Optional[str]
    '''刷新地图'''
    min: Optional[int]
    '''时间范围min'''
    max: Optional[int]
    '''时间范围max'''
    time: Optional[str]
    '''推送时间'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        self.map = data.get('map')
        self.min = data.get('min')
        self.max = data.get('max')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        log = f"马驹刷新推送：[{self.server}]的[{self.map}]将要在 {str(self.min)}-{str(self.max)} 分后刷新马驹。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[抓马监控] 时间：{self.time}\n{self.map} 将在[{self.min} - {self.max}分]后刷新马驹。"
        )


class HorseCatchedEvent(RecvEvent):
    '''马驹被抓事件'''
    __event__ = "WsRecv.HorseCatched"
    message_type = "HorseCatched"
    name: Optional[str]
    '''触发角色名'''
    map: Optional[str]
    '''地图'''
    horse: Optional[str]
    '''马驹名'''
    time: Optional[str]
    '''事件时间'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        self.map = data.get('map')
        self.name = data.get('name')
        self.horse = data.get('horse')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        log = f"马驹被抓事件：[{self.server}]的[{self.name}]在[{self.map}]捕获了 {self.horse} 。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[抓马监控] 时间：{self.time}\n{self.map} 的 {self.horse} 被 {self.name} 抓走了~"
        )


class FuyaoRefreshEvent(RecvEvent):
    '''扶摇开启事件'''
    __event__ = "WsRecv.FuyaoRefresh"
    message_type = "FuyaoRefresh"
    time: Optional[str]
    '''事件时间'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        log = f"扶摇刷新事件：[{self.server}]的扶摇开始刷新 。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[扶摇监控]\n扶摇九天在 {self.time} 开启了。"
        )


class FuyaoNamedEvent(RecvEvent):
    '''扶摇点名事件'''
    __event__ = "WsRecv.FuyaoNamed"
    message_type = "FuyaoNamed"
    names: Optional[List[str]]
    '''点名角色组'''
    time: Optional[str]
    '''点名时间'''

    def __init__(self, data: dict):
        '''
        重写初始化函数
        '''
        super().__init__()
        self.server = data.get('server')
        self.names = data.get('name')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        name = ",".join(self.names)
        log = f"扶摇点名事件：[{self.server}]的扶摇点名了，玩家[{name}] 。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        name = ",".join(self.names)
        return Message(
            f"[扶摇监控] 时间：{self.time}\n唐文羽点名了[{name}]。"
        )


def ws_event_factory(_type: int, data: dict) -> Optional[RecvEvent]:
    '''接收事件工厂，根据type创建对应事件'''
    # 开服推送
    if _type == 2011:
        return ServerStatusEvent(data)
    # 新闻推送
    if _type == 2012:
        return NewsRecvEvent(data)
    # 奇遇推送
    if _type == 2000:
        return SerendipityEvent(data)
    # 马驹刷新
    if _type == 2001:
        return HorseRefreshEvent(data)
    # 马驹捕获
    if _type == 2002:
        return HorseCatchedEvent(data)
    # 扶摇刷新
    if _type == 2003:
        return FuyaoRefreshEvent(data)
    # 扶摇点名
    if _type == 2004:
        return FuyaoNamedEvent(data)
    return None
