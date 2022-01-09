from typing import Union


class GroupList_Async():
    '''异步计数器，用于群发消息，支持list[int]和list[dict]，返回的是group_id'''

    def __init__(self, obj: Union[list, dict]):
        if isinstance(obj[0], int):
            self._it = iter(obj)
            return
        if isinstance(obj[0], dict):
            group_id_list = [one['group_id'] for one in obj]
            self._it = iter(group_id_list)

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
