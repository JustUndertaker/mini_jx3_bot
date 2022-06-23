import time
from typing import Optional, Tuple

from httpx import AsyncClient
from src.modules.search_record import SearchRecord
from src.modules.ticket_info import TicketInfo
from src.utils.log import logger

from .jx3api import JX3API


class TicketManager:
    '''
    ticket管理器，用来获取和验证ticket
    '''

    @classmethod
    async def check_ticket(cls, ticket: str, app: JX3API) -> bool:
        '''
        说明:
            检查ticket有效性

        参数:
            * `ticket`：ticket字符串
            * `app`：jx3api封装

        返回:
            * `bool`：ticket是否有效
        '''
        respone = await app.token_ticket(ticket=ticket)
        return respone.code == 200

    @classmethod
    async def get_ticket(cls) -> Optional[str]:
        '''获取一条有效的ticket，如果没有则返回None'''
        return await TicketInfo.get_ticket()

    @classmethod
    async def append_ticket(cls, ticket: str) -> bool:
        '''添加一条ticket，重复添加会返回false'''
        return await TicketInfo.append_ticket(ticket)


class SearchManager(object):
    '''查询管理器，负责查询记录和cd，负责搓app'''

    _main_site: str
    '''jx3api主站url'''

    def __init__(self):
        self._main_site = config.jx3api['jx3_url']

    def get_search_url(self, app: JX3APP) -> str:
        '''获取app请求地址'''
        return self._main_site+app.value.url

    async def search_record(self, group_id: int, app: JX3APP) -> Tuple[bool, int]:
        '''是否能够查询'''
        time_last = await SearchRecord.get_search_time(group_id, app.name)
        time_now = int(time.time())
        cd_time: int = app.value.cd
        over_time = over_time = time_now-time_last
        if over_time > cd_time:
            return True, 0
        left_cd = cd_time-over_time
        return False, left_cd

    async def search_once(self, group_id: int, app: JX3APP):
        '''查询app一次'''
        await SearchRecord.use_search(group_id, app.name)


ticket_manager = TicketManager()
'''ticket管理器'''
