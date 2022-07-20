import json
from typing import Optional

from tortoise import fields
from tortoise.models import Model

from src.config import default_config
from src.params import GroupSetting, NoticeType


def encode_text(text: str):
    data = [{"type": "text", "data": text}]
    return json.dumps(data, ensure_ascii=False)


class GroupInfo(Model):
    """群信息处理"""

    group_id = fields.IntField(pk=True)
    """群id"""
    group_name = fields.CharField(max_length=255, default="")
    """群名"""
    sign_nums = fields.IntField(default=0)
    """签到次数"""
    server = fields.CharField(max_length=255, default=default_config.server)
    """绑定服务器"""
    robot_status = fields.BooleanField(default=default_config.robot_status)
    """机器人状态"""
    robot_active = fields.IntField(default=default_config.robot_active)
    """活跃值"""
    welcome_status = fields.BooleanField(default=default_config.robot_welcome_status)
    """进群通知开关"""
    welcome_text = fields.JSONField(default=encode_text(default_config.robot_welcome))
    """进群通知内容"""
    someoneleft_status = fields.BooleanField(
        default=default_config.robot_someone_left_status
    )
    """离群通知开关"""
    someoneleft_text = fields.JSONField(
        default=encode_text(default_config.robot_someone_left)
    )
    """离群通知内容"""
    goodnight_status = fields.BooleanField(
        default=default_config.robot_goodnight_status
    )
    """晚安通知开关"""
    goodnight_text = fields.JSONField(
        default=encode_text(default_config.robot_goodnight)
    )
    """晚安通知内容"""
    ws_server = fields.BooleanField(default=True)
    """ws-开服推送开关"""
    ws_news = fields.BooleanField(default=True)
    """ws-新闻推送开关"""
    ws_serendipity = fields.BooleanField(default=True)
    """ws-奇遇推送开关"""
    ws_horse = fields.BooleanField(default=True)
    """ws-抓马推送开关"""
    ws_fuyao = fields.BooleanField(default=True)
    """ws-扶摇推送开关"""

    class Meta:
        table = "group_info"
        table_description = "管理QQ群信息"

    @classmethod
    async def group_init(cls, group_id: int, group_name: str):
        """
        说明:
            给一个群注册数据，刷新群名

        参数:
            * `group_id`：群号
            * `group_name`：群名
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        record.group_name = group_name
        await record.save(update_fields=["group_name"])

    @classmethod
    async def get_bot_status(cls, group_id: int) -> bool:
        """
        说明:
            获取机器人开启情况

        参数:
            * `group_id`：群号

        返回:
            * `bool`：机器人是否开启
        """
        record = await cls.get_or_none(group_id=group_id)
        return record.robot_status

    @classmethod
    async def group_sign_in(cls, group_id: int) -> int:
        """
        说明:
            群内签到，返回已签到数量

        参数:
            * `group_id`：群号

        返回:
            * `int`：当天已签到数量
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        record.sign_nums += 1
        await record.save(update_fields=["sign_nums"])
        return record.sign_nums

    @classmethod
    async def get_server(cls, group_id: int) -> str:
        """
        说明:
            获取绑定服务器

        参数:
            * `group_id`：群号

        返回:
            * `str`：服务器名
        """
        record = await cls.get_or_none(group_id=group_id)
        return record.server

    @classmethod
    async def get_config_status(cls, group_id: int, setting_type: GroupSetting) -> bool:
        """
        说明:
            获取群设置开关

        参数:
            * `group_id`：群号
            * `setting_type`：群设置枚举

        返回:
            * `bool`：开关状态
        """
        record = await cls.get_or_none(group_id=group_id)
        match setting_type:
            case GroupSetting.进群通知:
                status = record.welcome_status
            case GroupSetting.离群通知:
                status = record.someoneleft_status
            case GroupSetting.晚安通知:
                status = record.goodnight_status
            case GroupSetting.开服推送:
                status = record.ws_server
            case GroupSetting.新闻推送:
                status = record.ws_news
            case GroupSetting.奇遇推送:
                status = record.ws_serendipity
            case GroupSetting.抓马监控:
                status = record.ws_horse
            case GroupSetting.扶摇监控:
                status = record.ws_fuyao
        return status

    @classmethod
    async def set_config_status(
        cls, group_id: int, setting_type: GroupSetting, status: bool
    ) -> bool:
        """
        说明:
            设置群内容开关

        参数:
            * `group_id`：群号
            * `setting_type`：群设置枚举
            * `status`：开关状态
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        match setting_type:
            case GroupSetting.进群通知:
                record.welcome_status = status
            case GroupSetting.离群通知:
                record.someoneleft_status = status
            case GroupSetting.晚安通知:
                record.goodnight_status = status
            case GroupSetting.开服推送:
                record.ws_server = status
            case GroupSetting.新闻推送:
                record.ws_news = status
            case GroupSetting.奇遇推送:
                record.ws_serendipity = status
            case GroupSetting.抓马监控:
                record.ws_horse = status
            case GroupSetting.扶摇监控:
                record.ws_fuyao = status
            case _:
                return False
        await record.save()
        return True

    @classmethod
    async def reset_sign_nums(cls):
        """
        说明:
            重置所有群签到人数
        """
        await cls.all().update(sign_nums=0)

    @classmethod
    async def bind_server(cls, group_id: int, server: str):
        """
        说明:
            给群绑定服务器

        参数:
            * `group_id`：群号
            * `server`：服务器名
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        record.server = server
        await record.save(update_fields=["server"])

    @classmethod
    async def set_activity(cls, group_id: int, activity: int):
        """
        说明:
            给群设置活跃值
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        record.robot_active = activity
        await record.save(update_fields=["robot_active"])

    @classmethod
    async def set_status(cls, group_id: int, status: bool):
        """
        说明:
            设置某个群机器人总开关
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        record.robot_status = status
        await record.save(update_fields=["robot_status"])

    @classmethod
    async def get_meau_data(cls, group_id: int) -> dict:
        """
        说明:
            获取菜单数据

        参数:
            * `group_id`：群号

        返回:
            * `dict`：菜单数据字典
                * `robot_status` `bool`：机器人开关
                * `sign_nums` `int`：当天签到人数
                * `server` `str：`当前绑定服务器
                * `robot_active` `int`：机器人活跃度
                * `welcome_status` `bool`：进群通知开关
                * `someoneleft_status` `bool`：离群通知开关
                * `goodnight_status` `bool`：晚安通知开关
                * `ws_server` `bool`：ws开服推送开关
                * `ws_news` `bool`：ws新闻推送开关
                * `ws_serendipity` `bool`：ws奇遇推送开关
                * `ws_horse` `bool`：ws抓马推送开关
                * `ws_fuyao` `bool`：ws扶摇推送开关
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        return {
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

    @classmethod
    async def set_notice_msg(
        cls, group_id: int, notice_type: NoticeType, message: list[dict]
    ):
        """
        说明:
            设置通知内容

        参数:
            * `group_id`：群号
            * `notice_type`：通知类型
            * `message`：通知内容
        """
        _message = json.dumps(message, ensure_ascii=False)
        record, _ = await cls.get_or_create(group_id=group_id)
        match notice_type:
            case NoticeType.晚安通知:
                record.goodnight_text = _message
            case NoticeType.离群通知:
                record.someoneleft_text = _message
            case NoticeType.进群通知:
                record.welcome_text = _message
        await record.save()

    @classmethod
    async def get_notice_msg(cls, group_id: int, notice_type: NoticeType) -> list[dict]:
        """
        说明:
            获取通知内容

        参数:
            * `group_id`：群号
            * `notice_type`：通知类型

        返回:
            * `list[dict]`：消息数组
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        match notice_type:
            case NoticeType.晚安通知:
                data = record.goodnight_text
            case NoticeType.离群通知:
                data = record.someoneleft_text
            case NoticeType.进群通知:
                data = record.welcome_text
        return data

    @classmethod
    async def delete_group(cls, group_id: int):
        """
        说明:
            注销一个群的所有信息，退群时使用

        参数:
            * `group_id`：群号
        """
        await cls.filter(group_id=group_id).delete()

    @classmethod
    async def get_group_list(cls) -> list[dict]:
        """
        说明:
            获取群列表数据

        返回:
            * `list[dict]`：群信息列表
                * `group_id` `int`：qq群号
                * `group_name` `str`：群名
                * `sign_nums` `int`：当天签到数量
                * `server` `str`：绑定服务器名
                * `robot_status` `bool`：机器人总开关
                * `robot_active` `int`：机器人活跃度
        """
        return await cls.all().values(
            "group_id",
            "group_name",
            "sign_nums",
            "server",
            "robot_status",
            "robot_active",
        )

    @classmethod
    async def get_group_name(cls, group_id: int) -> Optional[str]:
        """
        说明:
            获取群名接口

        参数:
            * `group_id`：群号

        返回:
            * `Optional[str]`：群名
        """
        record = await cls.get_or_none(group_id=group_id)
        if record:
            return record.group_name
        return None

    @classmethod
    async def get_bot_active(cls, group_id: int) -> int:
        """
        说明:
            获取群机器人活跃值

        参数:
            * `group_id`：群号

        返回:
            * `int`：活跃值，1-99
        """
        record, _ = await cls.get_or_create(group_id=group_id)
        return record.robot_active
