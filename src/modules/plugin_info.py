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
    usage = fields.CharField(max_length=255)
    '''使用命令'''
    description = fields.CharField(max_length=255)
    '''插件描述'''
    status = fields.BooleanField(default=False)
    '''插件状态'''

    class Meta:
        table = "plugin_info"
        table_description = "用来记录插件状态"

    @ classmethod
    async def check_inited(cls, group_id: int, module_name: str) -> bool:
        '''
        说明:
            检查是否注册过插件

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名

        返回:
            * `bool`：是否注册该插件
        '''
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        return record is not None

    @ classmethod
    async def init_plugin(cls,
                          group_id: int,
                          module_name: str,
                          plugin_name: str,
                          description: str,
                          usage: str,
                          status: bool
                          ):
        '''
        说明:
            为一个群注册一条插件
        '''
        await cls.create(
            group_id=group_id,
            module_name=module_name,
            plugin_name=plugin_name,
            description=description,
            usage=usage,
            status=status
        )

    @classmethod
    async def get_plugin_status(cls, group_id: int, module_name: str) -> bool | None:
        '''
        说明:
            获取一个插件开关状态

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名

        返回:
            * `bool | None`：插件开关，为None时未找到该插件
        '''
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        return record.status if record else None

    @classmethod
    async def set_plugin_status(cls, group_id: int, module_name: str, status: bool) -> bool:
        '''
        说明:
            设置一个插件的开关状态

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名
            * `status`：开关

        返回:
            * `bool`：设置是否成功，未找到插件则不成功
        '''
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        if record:
            record.status = status
            await record.save()
            return True
        return False

    @classmethod
    async def get_meau_data(cls, group_id: int) -> list[dict]:
        '''
        说明:
            获取插件菜单数据

        参数:
            * `group_id`：群号

        返回:
            * `list[dict]`：插件菜单数据，以plugin_name排序
                * `plugin_name` `str`：插件名
                * `description` `str`：插件描述
                * `usage` `str`：插件用法
                * `status` `bool`：插件开关
        '''
        return await cls.filter(group_id=group_id).order_by("plugin_name").values(
            "plugin_name",
            "description",
            "usage",
            "status"
        )

    @classmethod
    async def delete_group(cls, group_id: int):
        '''
        说明:
            注销一个群的所有插件

        参数:
            * `group_id`：群号
        '''
        await cls.filter(group_id=group_id).delete()
