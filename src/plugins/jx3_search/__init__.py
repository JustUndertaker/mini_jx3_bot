from nonebot import export, on_regex
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

Export = export()
Export.plugin_name = "剑三查询"
Export.plugin_command = "参考“帮助”"
Export.plugin_usage = "剑三游戏查询，数据源使用jx3api"
Export.default_status = True
