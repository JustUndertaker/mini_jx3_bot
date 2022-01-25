from typing import List, Optional

from tortoise import fields
from tortoise.models import Model


class PluginInfo(Model):
    '''插件状态表'''
    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    '''QQ群号'''
    module_name = fields.CharField(max_length=255)
    '''模块名称'''
    plugin_name = fields.CharField(max_length=255)
    '''插件名称'''
    command = fields.CharField(max_length=255)
    '''使用命令'''
    usage = fields.CharField(max_length=255)
    '''插件描述'''
    status = fields.BooleanField(default=False)
    '''插件状态'''

    class Meta:
        table = "plugin_info"
        table_description = "用来记录插件状态"

    @ classmethod
    async def check_inited(cls, group_id: int, module_name: str) -> bool:
        '''检查是否注册过插件'''
        record = await PluginInfo.get_or_none(group_id=group_id, module_name=module_name)
        return not(record is None)

    @ classmethod
    async def init_plugin(cls,
                          group_id: int,
                          module_name: str,
                          plugin_name: str,
                          command: str,
                          usage: str,
                          status: bool
                          ) -> None:
        '''为某个群注册插件'''
        if command is None:
            command = ""
        if usage is None:
            usage = ""
        if status is None:
            status = False
        await PluginInfo.create(
            group_id=group_id,
            module_name=module_name,
            plugin_name=plugin_name,
            command=command,
            usage=usage,
            status=status
        )

    @classmethod
    async def get_plugin_status(cls, group_id: int, module_name: str) -> Optional[bool]:
        '''获取插件状态'''
        record = await PluginInfo.get_or_none(group_id=group_id, module_name=module_name)
        return record.status if record else None

    @classmethod
    async def set_plugin_status(cls, group_id: int, module_name: str, status: bool) -> bool:
        '''设置插件状态'''
        record = await PluginInfo.get_or_none(group_id=group_id, module_name=module_name)
        if record:
            record.status = status
            await record.save(update_fields=["status"])
            return True
        return False

    @classmethod
    async def get_meau_data(cls, group_id: int) -> List[dict]:
        '''获取菜单数据'''
        return await cls.filter(group_id=group_id).order_by("plugin_name").values("plugin_name", "command", "usage", "status")

    @classmethod
    async def delete_group(cls, group_id: int):
        '''删除群'''
        await cls.filter(group_id=group_id).delete()
