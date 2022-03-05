from typing import List, Tuple

from httpx import AsyncClient
from src.modules.group_info import GroupInfo
from src.modules.ticket_info import TicketInfo
from src.utils.config import config


async def get_group_list() -> List[dict]:
    '''
    获取群数据

    :返回
        * list[dict] 字段如下：
        * ``group_id`` 群id
        * ``group_name`` 群名
        * ``server`` 绑定服务器
        * ``robot_status`` 机器人开关
        * ``sign_nums`` 签到次数
        * ``robot_active`` 活跃值
    '''
    return await GroupInfo.get_group_list()


async def get_group(group_id: int) -> Tuple[bool, str]:
    '''获取群是否注册'''
    return await GroupInfo.check_group_init(group_id)


async def set_bot_status(group_id: int, status: str):
    '''设置机器人状态'''
    await GroupInfo.set_status(group_id, status)


async def get_ticket_list() -> List[dict]:
    '''获取ticket列表'''
    return await TicketInfo.get_all()


async def add_ticket(ticket: str) -> Tuple[bool, str]:
    '''添加一条ticket'''
    base_url = config.jx3api['jx3_url']
    url = f"{base_url}/token/ticket"
    params = {
        'ticket': ticket
    }
    async with AsyncClient() as client:
        try:
            req_url = await client.get(url=url, params=params)
            req = req_url.json()
            code = req['code']
            if code == 200:
                await TicketInfo.append_ticket(ticket)
                return True, ""
            else:
                return False, req['msg']
        except Exception as e:
            return False, str(e)


async def delete_ticket(id: int) -> bool:
    '''删除ticket'''
    return await TicketInfo.del_ticket(id)


async def clean_ticket():
    '''清理ticket'''
    await TicketInfo.clean_ticket()
