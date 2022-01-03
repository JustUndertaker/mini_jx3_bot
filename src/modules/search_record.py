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
