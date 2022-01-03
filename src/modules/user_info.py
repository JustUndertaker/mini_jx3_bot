from tortoise import fields
from tortoise.models import Model


class UserInfo(Model):
    '''用户表'''
    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    '''所属QQ群号'''
    user_id = fields.IntField()
    '''用户QQ号'''
    user_name = fields.CharField(max_length=255, default="")
    '''用户昵称'''
    gold = fields.IntField(default=0)
    '''用户金币'''
    friendly = fields.IntField(default=0)
    '''好感度'''
    lucky = fields.IntField(default=1)
    '''今日运势'''
    sign_times = fields.IntField(default=0)
    '''累计签到次数'''
    last_sign = fields.DateField(default="1970-1-1")
    '''上次签到日期'''

    class Meta:
        table = "user_info"
        table_description = "管理用户"
