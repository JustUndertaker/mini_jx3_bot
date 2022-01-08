from typing import Optional

from tortoise import fields
from tortoise.models import Model


class TicketInfo(Model):
    '''存储ticket表'''
    ticket = fields.CharField(max_length=255, pk=True)
    '''ticket值'''
    alive = fields.BooleanField(null=True, default=True)
    '''存活'''

    class Meta:
        table = "ticket_info"
        table_description = "存储推栏的ticket用"

    @classmethod
    async def get_ticket(cls) -> Optional[str]:
        '''获取一条有效的ticket，如果没有则返回None'''
        record = await cls.filter(alive=True)
        if record:
            return record[0].ticket
        return None

    @classmethod
    async def del_ticket(cls, ticket: str) -> bool:
        '''删除一条ticket'''
        record = await TicketInfo.get_or_none(ticket=ticket)
        if record:
            await record.delete()
            return True
        return False

    @classmethod
    async def clean_ticket(cls):
        '''清理所有'''
        await TicketInfo.filter(alive=False).delete()

    @classmethod
    async def append_ticket(cls, ticket: str) -> bool:
        '''添加一条ticket'''
        _, flag = await TicketInfo.get_or_create(ticket=ticket)
        return not flag

    @classmethod
    async def get_all(cls) -> list[dict]:
        '''
        :说明
            获取所有ticket
        :返回
            * list[dict]
            * ``"ticket"``：ticket值
            * ``"alive"``：是否有效
        '''
        return await TicketInfo.all().values("ticket", "alive")
