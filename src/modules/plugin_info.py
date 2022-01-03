from tortoise import fields
from tortoise.models import Model


class PluginInfo(Model):
    '''插件状态表'''
    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    '''QQ群号'''
    module_name = fields.CharField(max_length=255)
    '''插件名称'''
    description = fields.CharField(max_length=255, default='')
    '''插件描述'''
    status = fields.BooleanField(null=True, default=False)
    '''插件状态'''

    class Meta:
        table = "plugin_info"
        table_description = "用来记录插件状态"
