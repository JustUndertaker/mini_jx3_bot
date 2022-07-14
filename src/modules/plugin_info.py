from typing import Optional

from tortoise import fields
from tortoise.models import Model


class PluginInfo(Model):
    """插件状态表"""

    id = fields.IntField(pk=True, generated=True)
    group_id = fields.IntField()
    """QQ群号"""
    module_name = fields.CharField(max_length=255)
    """模块名称"""
    status = fields.BooleanField(default=False)
    """插件状态"""

    class Meta:
        table = "plugin_info"
        table_description = "用来记录插件开关"

    @classmethod
    async def check_inited(cls, group_id: int, module_name: str) -> bool:
        """
        说明:
            检查是否注册过插件

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名

        返回:
            * `bool`：是否注册该插件
        """
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        return record is not None

    @classmethod
    async def init_plugin(
        cls,
        group_id: int,
        module_name: str,
        status: bool,
    ):
        """
        说明:
            为一个群注册一条插件
        """
        await cls.create(
            group_id=group_id,
            module_name=module_name,
            status=status,
        )

    @classmethod
    async def get_plugin_status(cls, group_id: int, module_name: str) -> Optional[bool]:
        """
        说明:
            获取一个插件开关状态

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名

        返回:
            * `Optional[bool]`：插件开关，为None时未找到该插件
        """
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        return record.status if record else None

    @classmethod
    async def set_plugin_status(
        cls, group_id: int, module_name: str, status: bool
    ) -> bool:
        """
        说明:
            设置一个插件的开关状态

        参数:
            * `group_id`：群号
            * `module_name`：插件模块名
            * `status`：开关

        返回:
            * `bool`：设置是否成功，未找到插件则不成功
        """
        record = await cls.get_or_none(group_id=group_id, module_name=module_name)
        if record:
            record.status = status
            await record.save()
            return True
        return False

    @classmethod
    async def get_group_plugin_status(cls, group_id: int) -> list[dict]:
        """
        说明:
            获取一个群的所有插件的开关状态

        参数:
            * `group_id`：群号

        返回:
            * `list[dict]`：群的所有插件的开关状态，以module_name排序
                * `module_name` `str`：插件模块名
                * `status` `bool`：插件开关
        """
        return (
            await cls.filter(group_id=group_id)
            .order_by("module_name")
            .values("module_name", "status")
        )

    @classmethod
    async def delete_group(cls, group_id: int):
        """
        说明:
            注销一个群的所有插件

        参数:
            * `group_id`：群号
        """
        await cls.filter(group_id=group_id).delete()
