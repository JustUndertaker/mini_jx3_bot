from typing import Optional, Tuple

from src.modules.group_info import GroupInfo
from src.utils.log import logger

from .model import jx3_searcher, ticket_manager


async def get_server(group_id: int) -> str:
    '''获取群绑定的区服'''
    return await GroupInfo.get_server(group_id)


async def get_main_server(server: str) -> Optional[str]:
    '''获取主服务器'''
    return await jx3_searcher.get_server(server)


async def get_data_from_api(app_name: str, group_id: int, params: dict, need_ticket: bool = False) -> Tuple[str, dict]:
    '''
    :说明
        从jx3api获取内容

    :参数
        * app_name：查询分类
        * group_id：QQ群号
        * params：参数字典
        * need_ticket：是否需要ticket

    :返回
        * str：返回信息，为"success"时成功
        * dict：返回数据data
    '''
    if need_ticket:
        # 获取ticket

        while True:
            ticket = ticket_manager.get_ticket()
            params["ticket"] = ticket
            if not ticket:
                return "未找到合适的ticket，请联系管理员", {}
            try:
                return await jx3_searcher.get_data_from_api(group_id, app_name, params)

            except Exception as e:
                logger.error(
                    f"查询遇到了问题：{str(e)}"
                )
                return f"遇到了问题：{str(e)}。", {}

    try:
        return await jx3_searcher.get_data_from_api(group_id, app_name, params)

    except Exception as e:
        logger.error(
            f"查询遇到了问题：{str(e)}"
        )
        return f"遇到了问题：{str(e)}。", {}

# -------------------------------------------------------------
# 返回数据处理阶段，处理api返回data，方便模板使用
# -------------------------------------------------------------


def handle_data_price(data: list[list[dict]]) -> dict:
    '''处理物价数据'''
    req_data = {}
    for one_data in data:
        try:
            get_data = one_data[0]
            zone = get_data['zone']
            req_data[zone] = one_data
        except IndexError:
            pass
    return req_data
