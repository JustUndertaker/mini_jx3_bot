import time

from tortoise import fields
from tortoise.models import Model


class SearchRecord(Model):
    '''查询使用记录表'''
    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    '''群号'''
    app_name = fields.CharField(max_length=255)
    '''查询类型'''
    count = fields.IntField(default=0)
    '''查询次数'''
    last_time = fields.IntField(default=0)
    '''上次查询时间'''

    class Meta:
        table = "search_record"
        table_description = "记录查询次数"

    @classmethod
    async def get_search_time(cls, group_id: int, app_name: str) -> bool:
        '''获取上次查询记录时间'''
        record, _ = await SearchRecord.get_or_create(group_id=group_id, app_name=app_name)
        return record.last_time

    @classmethod
    async def use_search(cls, group_id: int, app_name: str):
        '''使用一次查询'''
        record, _ = await SearchRecord.get_or_create(group_id=group_id, app_name=app_name)
        time_now = int(time.time())
        record.last_time = time_now
        record.count += 1
        await record.save(update_fields=["last_time", "count"])

    @classmethod
    async def delete_group(cls, group_id: int):
        '''删除群'''
        await cls.filter(group_id=group_id).delete()
