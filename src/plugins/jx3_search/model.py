import time
from typing import Dict, Optional, Tuple, Union

from httpx import AsyncClient
from src.modules.search_record import SearchRecord
from src.modules.ticket_info import TicketInfo
from src.utils.config import config
from src.utils.log import logger

from .config import JX3_APP


class TicketManager(object):
    '''ticket管理器类'''
    _client: AsyncClient
    '''异步请求客户端'''
    _check_url: str
    '''检测ticket有效性接口'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(TicketManager, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 设置header
        token = config.jx3api['jx3_token']
        if token is None:
            token = ""
        headers = {"token": token, "User-Agent": "Nonebot2-jx3_bot"}
        self._client = AsyncClient(headers=headers)
        self._check_url = config.jx3api['jx3_url']+"/token/validity"

    async def check_ticket(self, ticket: str) -> bool:
        '''检查ticket的有效性'''
        params = {"ticket": ticket}
        try:
            req_url = await self._client.get(url=self._check_url, params=params)
            req = req_url.json()
            if req['code'] == 200:
                return True
            return False
        except Exception as e:
            logger.error(
                f"<r>查询ticket失败</r> | <g>{str(e)}</g>"
            )
            return False

    async def get_ticket(self) -> Optional[str]:
        '''获取一条有效的ticket，如果没有则返回None'''
        return await TicketInfo.get_ticket()

    async def append_ticket(self, ticket: str) -> bool:
        '''添加一条ticket，重复添加会返回false'''
        return await TicketInfo.append_ticket(ticket)


class SearchManager(object):
    '''查询管理器，负责查询记录和cd，负责搓app'''

    _main_site: str
    '''jx3api主站url'''
    _app_dict: Dict[str, Dict[str, Union[str, int]]]
    '''app字典'''

    def __init__(self):
        self._main_site = config.jx3api['jx3_url']
        self._app_dict = JX3_APP

    def _get_cd_time(self, app_name: str) -> int:
        '''获取app的冷却时间'''
        app = self._app_dict.get(app_name)
        if app:
            return app.get("cd")
        raise KeyError("未找到该app")

    def get_search_url(self, app_name: str) -> str:
        '''获取app请求地址'''
        app = self._app_dict.get(app_name)
        if app:
            return self._main_site+app.get("app")
        raise KeyError("未找到该app")

    async def search_record(self, group_id: int, app_name: str) -> Tuple[bool, int]:
        '''是否能够查询'''
        time_last = await SearchRecord.get_search_time(group_id, app_name)
        time_now = int(time.time())
        cd_time = self._get_cd_time(app_name)
        over_time = over_time = time_now-time_last
        if over_time > cd_time:
            return True, 0
        left_cd = cd_time-over_time
        return False, left_cd

    async def search_once(self, group_id: int, app_name: str):
        '''查询app一次'''
        await SearchRecord.use_search(group_id, app_name)


class Jx3Searcher(object):
    '''剑三查询类'''

    _client: AsyncClient
    '''异步请求客户端'''
    _search_manager = SearchManager()
    '''查询管理器'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(Jx3Searcher, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 设置header
        token = config.jx3api['jx3_token']
        if token is None:
            token = ""
        headers = {"token": token, "User-Agent": "Nonebot2-jx3_bot"}
        self._client = AsyncClient(headers=headers)

    async def get_server(self, server: str) -> Optional[str]:
        '''获取主服务器'''
        url = self._search_manager.get_search_url("server")
        params = {"name": server}
        try:
            req = await self._client.get(url=url, params=params)
            req_json = req.json()
            msg = req_json['msg']
            if msg == "success":
                return req_json['data']['server']
            return None
        except Exception as e:
            logger.error(
                f"查询主从服务器失败，原因：{str(e)}"
            )
            return None

    async def get_data_from_api(self, group_id: int, app_name: str, params: dict) -> Tuple[str, dict]:
        '''
        :说明
            从jx3api获取数据

        :参数
            * group_id：QQ群号
            * app_name：应用名称
            * params：参数

        :返回
            * str：返回消息
            * dict：网站返回数据
        '''
        # 判断cd
        flag, cd_time = await self._search_manager.search_record(group_id, app_name)
        if not flag:
            logger.debug(
                f"<y>群{group_id}</y> | <g>{app_name}</g> | 冷却中：{cd_time}"
            )
            msg = f"[{app_name}]冷却中（{cd_time}）"
            return msg, {}

        # 记录一次查询
        await self._search_manager.search_once(group_id, app_name)
        # 获取url
        url = self._search_manager.get_search_url(app_name)
        try:
            req = await self._client.get(url=url, params=params)
            req_json: dict = req.json()
            msg: str = req_json['msg']
            data = req_json['data']
            logger.debug(
                f"<y>群{group_id}</y> | <g>{app_name}</g> | 返回：{data}"
            )
            return msg, data
        except Exception as e:
            error = str(e)
            logger.error(
                f"<y>群{group_id}</y> | <g>{app_name}</g> | 失败：{error}"
            )
            return error, {}


ticket_manager = TicketManager()
'''ticket管理器'''

jx3_searcher = Jx3Searcher()
'''剑三查询器'''
