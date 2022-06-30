from typing import Union


class GroupList_Async:
    """
    异步计数器，用于异步发送多个消息，支持dict,list使用方法：
    ```
    async for group_id in GroupList_Async(group_id_list):
        await bot.send_group_msg(group_id, message)

    async for user_id in GroupList_Async(superusers):
        await bot.send_private_msg(user_id, message)
    ```
    """

    def __init__(self, obj: Union[list, dict]):
        if isinstance(obj[0], int):
            self._it = iter(obj)
            return
        if isinstance(obj[0], str):
            self._it = iter(obj)
            return
        if isinstance(obj[0], dict):
            group_id_list = [one["group_id"] for one in obj]
            self._it = iter(group_id_list)

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        if isinstance(value, str):
            value = int(value)
        return value
