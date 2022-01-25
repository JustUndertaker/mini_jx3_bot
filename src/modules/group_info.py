import json
from typing import List, Literal, Optional, Tuple

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

    @classmethod
    async def get_config_status(cls, group_id: int,
                                config_type: Literal["welcome_status", "goodnight_status", "someoneleft_status"]
                                ) -> Optional[bool]:
        '''获取群设置开关'''
        record = await GroupInfo.get_or_none(group_id=group_id)
        if record:
            if config_type == "welcome_status":
                return record.welcome_status
            if config_type == "goodnight_status":
                return record.goodnight_status
            if config_type == "someoneleft_status":
                return record.someoneleft_status
        return None

    @classmethod
    async def set_config_status(cls, group_id: int,
                                config_type: Literal["welcome_status", "goodnight_status", "someoneleft_status", "ws_server", "ws_news", "ws_serendipity", "ws_horse", "ws_fuyao"],
                                status: bool
                                ) -> bool:
        '''设置群内容开关'''
        record = await GroupInfo.get_or_none(group_id=group_id)
        if record:
            if config_type == "welcome_status":
                record.welcome_status = status
                await record.save(update_fields=["welcome_status"])
            if config_type == "goodnight_status":
                record.goodnight_status = status
            if config_type == "someoneleft_status":
                record.someoneleft_status = status
            if config_type == "ws_server":
                record.ws_server = status
            if config_type == "ws_news":
                record.ws_news = status
            if config_type == "ws_serendipity":
                record.ws_serendipity = status
            if config_type == "ws_horse":
                record.ws_horse = status
            if config_type == "ws_fuyao":
                record.ws_fuyao = status
            await record.save(update_fields=[config_type])
            return True
        return False

    @classmethod
    async def reset_sign_nums(cls):
        '''重置签到人数'''
        await GroupInfo.all().update(sign_nums=0)

    @classmethod
    async def bind_server(cls, group_id: int, server: str):
        '''绑定服务器'''
        record, _ = await cls.get_or_create(group_id=group_id)
        record.server = server
        await record.save(update_fields=["server"])

    @classmethod
    async def set_activity(cls, group_id: int, activity: int):
        '''设置活跃值'''
        record, _ = await cls.get_or_create(group_id=group_id)
        record.robot_active = activity
        await record.save(update_fields=["robot_active"])

    @classmethod
    async def set_status(cls, group_id: int, status: bool):
        '''设置机器人开关'''
        record, _ = await cls.get_or_create(group_id=group_id)
        record.robot_status = status
        await record.save(update_fields=["robot_status"])

    @classmethod
    async def get_meau_data(cls, group_id: int) -> dict:
        '''获取菜单数据'''
        record, _ = await cls.get_or_create(group_id=group_id)
        data = {
            "robot_status": record.robot_status,
            "sign_nums": record.sign_nums,
            "server": record.server,
            "robot_active": record.robot_active,
            "welcome_status": record.welcome_status,
            "someoneleft_status": record.someoneleft_status,
            "goodnight_status": record.goodnight_status,
            "ws_server": record.ws_server,
            "ws_news": record.ws_news,
            "ws_serendipity": record.ws_serendipity,
            "ws_horse": record.ws_horse,
            "ws_fuyao": record.ws_fuyao,
        }
        return data

    @classmethod
    async def set_notice_msg(cls, group_id: int, notice_type: Literal["晚安通知", "离群通知", "进群通知"], message: List[dict]):
        '''设置通知内容'''
        _message = json.dumps(message, ensure_ascii=False)
        record, _ = await cls.get_or_create(group_id=group_id)
        if notice_type == "晚安通知":
            record.goodnight_text = _message
            await record.save(update_fields=["goodnight_text"])

        if notice_type == "离群通知":
            record.someoneleft_text = _message
            await record.save(update_fields=["someoneleft_text"])

        if notice_type == "进群通知":
            record.welcome_text = _message
            await record.save(update_fields=["welcome_text"])

    @classmethod
    async def get_notice_msg(cls, group_id: int, notice_type: Literal["晚安通知", "离群通知", "进群通知"]) -> List[dict]:
        '''获取通知内容'''
        record, _ = await cls.get_or_create(group_id=group_id)
        if notice_type == "晚安通知":
            return record.goodnight_text
        if notice_type == "离群通知":
            return record.someoneleft_text
        if notice_type == "进群通知":
            return record.welcome_text

    @classmethod
    async def delete_group(cls, group_id: int):
        '''注销群'''
        await cls.filter(group_id=group_id).delete()

    @classmethod
    async def get_group_list(cls) -> List[dict]:
        '''获取群列表数据'''
        return await cls.all().values("group_id", "group_name", "sign_nums", "server", "robot_status", "robot_active")

    @classmethod
    async def check_group_init(cls, group_id: int) -> Tuple[bool, str]:
        '''检测是否注册'''
        record = await cls.get_or_none(group_id=group_id)
        if record:
            return True, record.group_name
        return False, ""

    @classmethod
    async def get_bot_active(cls, group_id: int) -> int:
        '''获取活跃值'''
        record, _ = await cls.get_or_create(group_id=group_id)
        return record.robot_active
