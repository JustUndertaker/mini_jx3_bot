from nonebot.plugin import get_loaded_plugins
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo


async def group_init(group_id: int, group_name: str):
    '''注册群数据'''
    await GroupInfo.group_init(group_id, group_name)


async def load_plugins(group_id: int):
    '''给某个群默认加载插件'''
    # 注册过的不再注册
    flag = await PluginInfo.check_inited(group_id)
    if flag:
        return

    # 注册所有插件
    plugins = list(get_loaded_plugins())
    for one_plugin in plugins:
        export = one_plugin.export
        plugin_name = export.get("plugin_name")
        if plugin_name is None:
            continue

        await PluginInfo.init_plugin(group_id=group_id,
                                     module_name=one_plugin.name,
                                     plugin_name=plugin_name,
                                     command=export.get("plugin_command"),
                                     usage=export.get("plugin_usage"),
                                     status=export.get("default_status")
                                     )
