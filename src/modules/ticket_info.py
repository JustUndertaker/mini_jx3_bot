from tortoise import fields
from tortoise.models import Model


class TicketInfo(Model):
    '''存储ticket表'''
    id = fields.IntField(pk=True, generated=True)
    bot_id = fields.IntField()
    '''机器人QQ'''
    ticket = fields.CharField(max_length=255)
    '''token值'''
    alive = fields.BooleanField(null=True, default=True)
    '''存活'''

    class Meta:
        table = "token_info"
        table_description = "存储token用"
