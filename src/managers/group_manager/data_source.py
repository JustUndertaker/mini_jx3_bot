from pathlib import Path

from nonebot.adapters.onebot.v11 import Message, MessageSegment

from src.config import path_config
from src.internal.plugin_manager import plugin_manager
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.modules.search_record import SearchRecord
from src.modules.user_info import UserInfo
from src.params import NoticeType

from .model import ImageHandler


async def _message_encoder(message: Message, path: Path) -> list[dict]:
    """将message编码成json格式，将图片保存本地"""
    req_data = []
    index = 0
    for one in message:
        if one.type == "image":
            url = one.data["url"]
            file_name = path / f"{str(index)}.image"
            flag = await ImageHandler.save_image(file_name, url)
            if flag:
                index += 1
                data = {"type": "image", "data": str(file_name)}
                req_data.append(data)
            continue

        if one.type == "text":
            data = {"type": "text", "data": one.data["text"]}
            req_data.append(data)
            continue

        if one.type == "face":
            data = {"type": "face", "data": one.data["id"]}
            req_data.append(data)
            continue

    return req_data


async def message_decoder(group_id: int, notice_type: NoticeType) -> Message:
    """获取通知消息，并转换成Message"""
    msg = await GroupInfo.get_notice_msg(group_id, notice_type)
    message = Message()
    for one in msg:
        if one["type"] == "image":
            file_name = Path(one["data"])
            _data = await ImageHandler.load_image(file_name)
            data = MessageSegment.image(_data)
            message.append(data)
        if one["type"] == "text":
            data = MessageSegment.text(one["data"])
            message.append(data)
        if one["type"] == "face":
            data = MessageSegment.face(one["data"])
            message.append(data)
    return message


async def handle_data_notice(group_id: int, notice_type: NoticeType, message: Message):
    """处理通知内容"""
    _path = path_config.data
    # 创建文件夹
    path = Path(_path) / notice_type.name / str(group_id)
    if not path.exists():
        path.mkdir(parents=True)
    else:
        for one_file in path.iterdir():
            one_file.unlink()

    data = []
    msg0 = {"type": "text", "data": str(message.pop(0))[5:]}
    data.append(msg0)
    data += await _message_encoder(message, path)
    await GroupInfo.set_notice_msg(group_id, notice_type, data)


async def bot_group_quit(group_id):
    """退群处理"""
    # 注销group_inofo
    await GroupInfo.delete_group(group_id)
    # 注销plugin_info
    await PluginInfo.delete_group(group_id)
    # 注销user_info
    await UserInfo.delete_group(group_id)
    # 注销search_record
    await SearchRecord.delete_group(group_id)


async def get_meau_data(group_id: int) -> dict:
    """获取菜单数据"""
    req_data = {}
    req_data["group"] = await GroupInfo.get_meau_data(group_id)
    req_data["plugin"] = await plugin_manager.get_group_plugin_status(group_id)
    return req_data
