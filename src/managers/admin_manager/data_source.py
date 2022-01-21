from typing import Tuple

from src.modules.group_info import GroupInfo


async def get_group_list() -> list[dict]:
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
