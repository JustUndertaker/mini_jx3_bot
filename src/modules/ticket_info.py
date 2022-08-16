from typing import Optional

from tortoise import fields
from tortoise.models import Model


class TicketInfo(Model):
    """存储ticket表"""

    id = fields.IntField(pk=True, generated=True)
    ticket = fields.CharField(max_length=255)
    """ticket值"""
    alive = fields.BooleanField(null=True, default=True)
    """存活"""

    class Meta:
        table = "ticket_info"
        table_description = "存储推栏的ticket用"

    @classmethod
    async def get_ticket(cls) -> Optional[str]:
        """
        说明:
            获取一条有效的ticket，如果没有则返回None

        返回:
            * `Optional[str]`：ticket值，None则没有
        """
        record = await cls.filter(alive=True).first()
        # record = await cls.get_or_none(alive=True)
        if record:
            return record.ticket
        return None

    @classmethod
    async def del_ticket(cls, id: int) -> bool:
        """
        说明:
            删除一条ticket

        参数:
            * `id`：ticket的id编号

        返回:
            * `bool`：是否删除成功
        """
        record = await cls.get_or_none(id=id)
        if record:
            await record.delete()
            return True
        return False

    @classmethod
    async def clean_ticket(cls):
        """
        说明:
            清理所有无效ticket
        """
        await cls.filter(alive=False).delete()

    @classmethod
    async def append_ticket(cls, ticket: str) -> bool:
        """
        说明:
            添加一条ticket，不可以添加重复的ticket

        参数:
            * `ticket`：ticket字符串值

        返回:
            * `bool`：是否添加成功
        """
        _, flag = await cls.get_or_create(ticket=ticket)
        return not flag

    @classmethod
    async def get_all(cls) -> list[dict]:
        """
        说明:
            获取所有ticket

        返回:
            * `list[dict]`：ticket字典列表
                * `id` `int`：ticket编号
                * `ticket` `str`：ticket值
                * `alive` `bool`：是否有效
        """
        return await cls.all().values("id", "ticket", "alive")
