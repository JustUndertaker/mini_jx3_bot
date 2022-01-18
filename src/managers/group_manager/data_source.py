from typing import Optional

from httpx import AsyncClient
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo

from ..server_manager._websocket import ws_client


async def get_main_server(server: str) -> Optional[str]:
    '''获取主服务器'''
    params = {
        "name": server
    }
    url = "https://www.jx3api.com/app/server"
    async with AsyncClient() as client:
        try:
            req = await client.get(url=url, params=params)
            req_json = req.json()
            if req_json['code'] == 200:
                return req_json['data']['server']
            return None
        except Exception:
            return None


async def bind_server(group_id: int, server: str):
    '''绑定服务器'''
    await GroupInfo.bind_server(group_id, server)


async def set_activity(group_id: int, activity: int):
    '''设置活跃值'''
    await GroupInfo.set_activity(group_id, activity)


async def set_status(group_id: int, status: bool):
    '''设置机器人开关'''
    await GroupInfo.set_status(group_id, status)


async def get_meau_data(group_id: int) -> dict:
    '''获取菜单数据'''
    req_data = {}
    req_data['ws'] = ws_client.get_ws_status()
    req_data['group'] = await GroupInfo.get_meau_data(group_id)
    req_data['plugin'] = await PluginInfo.get_meau_data(group_id)
    return req_data
