import json
from typing import Literal, Optional

from src.utils.config import config
from tortoise import fields
from tortoise.models import Model


def encode_text(text: str):
    data = [{
        "type": "text",
        "data": text
    }]
    return json.dumps(data, ensure_ascii=False)


class GroupInfo(Model):
    '''群信息处理'''
    group_id = fields.IntField(pk=True)
    '''群id'''
    group_name = fields.CharField(max_length=255, default='')
    '''群名'''
    sign_nums = fields.IntField(default=0)
    '''签到次数'''
    server = fields.CharField(max_length=255, default=config.default['server'])
    '''绑定服务器'''
    robot_status = fields.BooleanField(default=config.default['robot_status'])
    '''机器人状态'''
    robot_active = fields.IntField(default=config.default['robot_active'])
    '''活跃值'''
    welcome_status = fields.BooleanField(default=config.default['robot_welcome_status'])
    '''进群通知开关'''
    welcome_text = fields.JSONField(default=encode_text(config.default['robot_welcome']))
    '''进群通知内容'''
    someoneleft_status = fields.BooleanField(default=config.default['robot_someone_left_status'])
    '''离群通知开关'''
    someoneleft_text = fields.JSONField(default=encode_text(config.default['robot_someone_left']))
    '''离群通知内容'''
    goodnight_status = fields.BooleanField(default=config.default['robot_goodnight_status'])
    '''晚安通知开关'''
    goodnight_text = fields.JSONField(default=encode_text(config.default['robot_goodnight']))
    '''晚安通知内容'''
    ws_server = fields.BooleanField(default=True)
    '''ws-开服推送开关'''
    ws_news = fields.BooleanField(default=True)
    '''ws-新闻推送开关'''
    ws_serendipity = fields.BooleanField(default=True)
    '''ws-奇遇推送开关'''
    ws_horse = fields.BooleanField(default=True)
    '''ws-抓马推送开关'''
    ws_fuyao = fields.BooleanField(default=True)
    '''ws-扶摇推送开关'''

    class Meta:
        table = "group_info"
        table_description = "管理QQ群信息"

    @classmethod
    async def group_init(cls, group_id: int, group_name: str):
        '''给一个群注册数据，刷新群名'''
        record, _ = await GroupInfo.get_or_create(group_id=group_id)
        record.group_name = group_name
        await record.save(update_fields=["group_name"])

    @classmethod
    async def get_bot_status(cls, group_id: int) -> Optional[bool]:
        '''获取机器人开启情况'''
        record = await GroupInfo.get_or_none(group_id=group_id)
        if record:
            return record.robot_status
        return None

    @classmethod
    async def group_sign_in(cls, group_id: int) -> int:
        '''群内签到，返回已签到数量'''
        record, _ = await GroupInfo.get_or_create(group_id=group_id)
        record.sign_nums += 1
        await record.save(update_fields=["sign_nums"])
        return record.sign_nums

    @classmethod
    async def get_server(cls, group_id: int) -> Optional[str]:
        '''获取绑定服务器'''
        record = await GroupInfo.get_or_none(group_id=group_id)
        return record.server if record else None

    @classmethod
    async def get_ws_status(cls, group_id: int,
                            recv_type: Literal["server", "news", "serendipity", "horse", "fuyao"]
                            ) -> Optional[bool]:
        '''获取ws通知状态'''
        record = await GroupInfo.get_or_none(group_id=group_id)
        if record:
            if recv_type == "server":
                return record.ws_server
            if recv_type == "news":
                return record.ws_news
            if recv_type == "serendipity":
                return record.ws_serendipity
            if recv_type == "horse":
                return record.ws_horse
            if recv_type == "fuyao":
                return record.ws_fuyao
        return None
