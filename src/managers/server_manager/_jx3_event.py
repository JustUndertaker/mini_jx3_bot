import time
from abc import abstractmethod
from datetime import datetime
from typing import Optional

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters.onebot.v12.message import Message
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
    '''ws推送事件'''
    __event__ = "WsRecv"
    post_type: str = "WsRecv"
    message_type: Optional[str]
    server: Optional[str] = None
    '''影响服务器'''

    @property
    @abstractmethod
    def log(self) -> str:
        '''事件日志内容'''
        raise NotImplementedError

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

    @staticmethod
    def create_event(_type: int, data: dict) -> Optional["RecvEvent"]:
        '''根据推送类型创建事件'''
        match _type:
            case 1001:
                # 奇遇播报
                return SerendipityEvent(data)
            case 1002:
                # 马驹刷新
                return HorseRefreshEvent(data)
            case 1003:
                # 马驹捕获
                return HorseCatchedEvent(data)
            case 1004:
                # 扶摇开启
                return FuyaoRefreshEvent(data)
            case 1005:
                # 扶摇点名
                return FuyaoNamedEvent(data)
            case 1006:
                # 烟花播报
                return FireworksEvent(data)
            case 1010:
                # 游戏消息
                return GameSysMsgEvent(data)
            case 2001:
                # 新闻监控
                return ServerStatusEvent(data)
            case 2002:
                # 新闻资讯
                return NewsRecvEvent(data)
            case 1506:
                # 订阅烟花回调消息
                return FireworkSubscribeEvent(data)
            case 1510:
                # 订阅游戏系统回调消息
                return GameSysSubscribeEvent(data)
            case 1606:
                # 取消订阅烟花回调消息
                return FireworkDisSubscribeEvent(data)
            case 1610:
                # 取消订阅系统回调消息
                return GameSysDisSubscribeEvent(data)
            case _:
                return None


class ServerStatusEvent(RecvEvent):
    '''服务器状态推送事件'''
    __event__ = "WsRecv.ServerStatus"
    message_type = "ServerStatus"
    status: Optional[bool]
    '''服务器状态'''

    def __init__(self, data: dict):
        '''
        服务器状态推送事件
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
        新闻推送事件
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
    '''奇遇播报事件'''
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
        奇遇播报事件
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
        马驹刷新事件
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
    '''马驹捕获事件'''
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
        马驹捕获事件
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
        扶摇开启事件
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
    names: Optional[list[str]]
    '''点名角色组'''
    time: Optional[str]
    '''点名时间'''

    def __init__(self, data: dict):
        '''
        扶摇点名事件
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


class FireworksEvent(RecvEvent):
    '''烟花播报时间'''
    __event__ = "WsRecv.Fireworks"
    message_type = "Fireworks"
    map: Optional[str]
    '''烟花地图'''
    name: Optional[str]
    '''接受烟花的角色'''
    sender: Optional[str]
    '''使用烟花的角色'''
    recipient: Optional[str]
    '''烟花名字'''
    time: Optional[str]
    '''烟花使用时间'''

    def __init__(self, data: dict):
        '''烟花播报时间'''
        super().__init__()
        self.server = data.get('server')
        self.map = data.get('map')
        self.name = data.get('name')
        self.sender = data.get('sender')
        self.recipient = data.get('recipient')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        log = f"烟花事件：{self.sender} 在 {self.map} 对 {self.name} 使用了烟花：{self.recipient}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[烟花监控] 时间：{self.time}\n{self.sender} 在 {self.map} 对 {self.name} 使用了烟花：{self.recipient}。"
        )


class GameSysMsgEvent(RecvEvent):
    '''游戏系统频道消息推送'''

    __event__ = "WsRecv.GameSysMsg"
    message_type = "GameSysMsg"
    message: Optional[str]
    '''消息内容'''
    time: Optional[str]
    '''消息时间'''

    def __init__(self, data: dict):
        '''游戏系统频道消息推送'''
        super().__init__()
        self.server = data.get('server')
        get_time = int(data.get('time'))
        start_trans = time.localtime(get_time)
        self.time = time.strftime('%H:%M:%S', start_trans)

    @property
    def log(self) -> str:
        log = f"系统频道推送：{self.message}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[系统频道推送]\n时间：{self.time}\n{self.message}。"
        )


class FireworkSubscribeEvent(RecvEvent):
    '''烟花订阅回执'''
    __event__ = "WsRecv.FireworkSubscribeEvent"
    message_type = "FireworkSubscribeEvent"
    server_list: list[str]
    '''已订阅服务器列表'''

    def __init__(self, data: dict):
        '''烟花订阅回执'''
        super().__init__()
        self.server_list = data.get('server')

    @property
    def log(self) -> str:
        log = f"烟花订阅回执，已订阅服务器：{self.server_list}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[烟花订阅回执]\n已订阅服务器：{self.server_list}。"
        )


class FireworkDisSubscribeEvent(RecvEvent):
    '''取消烟花订阅回执'''
    __event__ = "WsRecv.FireworkDisSubscribeEvent"
    message_type = "FireworkDisSubscribeEvent"
    server_list: list[str]
    '''已订阅服务器列表'''

    def __init__(self, data: dict):
        '''取消烟花订阅回执'''
        super().__init__()
        self.server_list = data.get('server')

    @property
    def log(self) -> str:
        log = f"取消烟花订阅回执，已订阅服务器：{self.server_list}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[取消烟花订阅回执]\n已订阅服务器：{self.server_list}。"
        )


class GameSysSubscribeEvent(RecvEvent):
    '''订阅游戏系统消息回执'''
    __event__ = "WsRecv.GameSysSubscribeEvent"
    message_type = "GameSysSubscribeEvent"
    server_list: list[str]
    '''已订阅服务器列表'''

    def __init__(self, data: dict):
        '''订阅游戏系统消息回执'''
        super().__init__()
        self.server_list = data.get('server')

    @property
    def log(self) -> str:
        log = f"订阅游戏系统消息回执，已订阅服务器：{self.server_list}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[订阅游戏系统消息回执]\n已订阅服务器：{self.server_list}。"
        )


class GameSysDisSubscribeEvent(RecvEvent):
    '''取消订阅游戏系统消息回执'''
    __event__ = "WsRecv.GameSysDisSubscribeEvent"
    message_type = "GameSysDisSubscribeEvent"
    server_list: list[str]
    '''已订阅服务器列表'''

    def __init__(self, data: dict):
        '''取消订阅游戏系统消息回执'''
        super().__init__()
        self.server_list = data.get('server')

    @property
    def log(self) -> str:
        log = f"取消订阅游戏系统消息回执，已订阅服务器：{self.server_list}。"
        return log

    @overrides(RecvEvent)
    def get_message(self) -> Message:
        return Message(
            f"[取消订阅游戏系统消息回执]\n已订阅服务器：{self.server_list}。"
        )
