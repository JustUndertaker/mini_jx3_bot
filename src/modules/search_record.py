import time

from tortoise import fields
from tortoise.models import Model


class SearchRecord(Model):
    """查询使用记录表"""

    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    """群号"""
    app_name = fields.CharField(max_length=255)
    """查询类型"""
    count = fields.IntField(default=0)
    """查询次数"""
    last_time = fields.IntField(default=0)
    """上次查询时间"""

    class Meta:
        table = "search_record"
        table_description = "记录查询次数"

    @classmethod
    async def get_search_time(cls, group_id: int, app_name: str) -> int:
        """
        说明:
            获取上次查询记录时间

        参数:
            * `group_id`：群号
            * `app_name`：app名称

        返回:
            * `int`：上次查询时间戳
        """
        record, _ = await cls.get_or_create(group_id=group_id, app_name=app_name)
        return record.last_time

    @classmethod
    async def use_search(cls, group_id: int, app_name: str):
        """
        说明:
            使用一次查询

        参数:
            * `group_id`：群号
            * `app_name`：app名称
        """
        record, _ = await cls.get_or_create(group_id=group_id, app_name=app_name)
        time_now = int(time.time())
        record.last_time = time_now
        record.count += 1
        await record.save()

    @classmethod
    async def delete_group(cls, group_id: int):
        """
        说明:
            删除一个群所有记录，注销时使用

        参数:
            * `group_id`：群号
        """
        await cls.filter(group_id=group_id).delete()
