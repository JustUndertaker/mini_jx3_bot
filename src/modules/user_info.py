import random
from datetime import date

from tortoise import fields
from tortoise.models import Model


class UserInfo(Model):
    """用户表"""

    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    """所属QQ群号"""
    user_id = fields.IntField()
    """用户QQ号"""
    user_name = fields.CharField(max_length=255, default="")
    """用户昵称"""
    gold = fields.IntField(default=0)
    """用户金币"""
    friendly = fields.IntField(default=0)
    """好感度"""
    lucky = fields.IntField(default=1)
    """今日运势"""
    sign_times = fields.IntField(default=0)
    """累计签到次数"""
    last_sign = fields.DateField(default=date(1970, 1, 1))
    """上次签到日期"""

    class Meta:
        table = "user_info"
        table_description = "管理用户"

    @classmethod
    async def user_init(cls, user_id: int, group_id: int, user_name: str):
        """
        说明:
            注册一个用户并刷新昵称

        参数:
            * `user_id`: 用户QQ号
            * `group_id`：群号
            * `user_name`：用户昵称
        """
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        record.user_name = user_name
        await record.save()

    @classmethod
    async def sign_in(
        cls,
        user_id: int,
        group_id: int,
        lucky_min: int,
        lucky_max: int,
        friendly_add: int,
        gold_base: int,
        lucky_gold: int,
    ) -> dict[str, int]:
        """
        说明:
            设置签到

        参数:
            * `user_id`：用户QQ
            * `group_id`：QQ群号
            * `lucky_min`：最小运势
            * `lucky_max`：最大运势
            * `friendly_add`：签到获取的好友度系数
            * `gold_base`：金币底薪
            * `lucky_gold`：幸运值影响因子

        返回:
            * `dict[str,int]`：返回数据字典
                * `today_lucky`：今日运势
                * `today_gold`：今日金币
                * `all_gold`：总金币
                * `all_friendly`：好友度
                * `sign_times`：签到次数
        """
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        # 设置签到日期
        today = date.today()
        record.last_sign = today
        # 计算运势
        today_lucky = random.randint(lucky_min, lucky_max)
        record.lucky = today_lucky
        # 计算金币
        today_gold = gold_base + lucky_gold * today_lucky
        record.gold += today_gold
        all_gold = record.gold
        # 计算好友度
        today_friendy = today_lucky * friendly_add
        record.friendly += today_friendy
        # 累计签到次数
        record.sign_times += 1
        await record.save()
        return {
            "today_lucky": today_lucky,
            "today_gold": today_gold,
            "all_gold": all_gold,
            "all_friendly": record.friendly,
            "sign_times": record.sign_times,
        }

    @classmethod
    async def get_last_sign(cls, user_id: int, group_id: int) -> date:
        """
        说明:
            获取上次签到时间

        参数:
            * `user_id`：用户qq
            * `group_id`：群号

        返回:
            * `date`：签到日期
        """
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        return record.last_sign

    @classmethod
    async def delete_group(cls, group_id: int):
        """
        说明:
            删除一个群的所有用户记录，注销时使用

        参数:
            * `group_id`：群号
        """
        await cls.filter(group_id=group_id).delete()

    @classmethod
    async def delete_user(cls, user_id: int, group_id: int):
        """
        说明:
            删除一条用户记录，用户退群时使用

        参数:
            * `user_id`：用户qq
            * `group_id`：群号
        """
        record = await cls.get_or_none(user_id=user_id, group_id=group_id)
        if record:
            await record.delete()

    @classmethod
    async def cost_gold(cls, user_id: int, group_id: int, gold: int) -> bool:
        """
        说明:
            使用一次金币，如果使用成功则返回True

        参数:
            * `user_id`：用户名
            * `group_id`：群号
            * `gold`：金币数量

        返回:
            * `bool`：是否使用成功
        """
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        if record.gold >= gold:
            record.gold -= gold
            await record.save()
            return True
        return False

    @classmethod
    async def get_user_data(cls, user_id: int, group_id: int) -> dict[str, int]:
        """
        说明:
            获取用户数据，查看用户当前的数据

        参数:
            * `user_id`：用户名
            * `group_id`：群号

        返回:
            * `dict[str,int]`：返回数据字典
                * `sign` `bool`：是否签到
                * `lucky`：今日运势
                * `gold`：金币
                * `friendly`：好友度
        """
        record, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        return {
            "sign": record.last_sign == date.today(),
            "lucky": record.lucky,
            "gold": record.gold,
            "friendly": record.friendly,
        }
