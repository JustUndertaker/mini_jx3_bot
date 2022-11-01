"""
插件管理器模块，用来管理插件
"""

from typing import Optional

from nonebot.plugin import Plugin, get_loaded_plugins

from src.modules.plugin_info import PluginInfo
from src.params import PluginConfig


class PluginManager:
    """插件管理器"""

    plugins: dict[str, Plugin] = {}
    """已管理插件映射集"""
    inited: bool = False
    """是否已初始化"""

    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, "_instance"):
            orig = super(PluginManager, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def init(self):
        """
        初始化加载插件，在第一次使用时需要用到
        """
        if self.inited:
            return
        loaded_plugins = list(get_loaded_plugins())
        for one_plugin in loaded_plugins:
            # 跳过没有元数据或者配置元数据内不受插件管理器管理的插件
            metadata = one_plugin.metadata
            if metadata is None:
                continue
            config: PluginConfig = metadata.config
            # 判断config是否为PluginConfig
            if not isinstance(config, PluginConfig):
                continue

            # 判断是否受管理
            if not config.enable_managed:
                continue

            # 储存所有受管理插件
            self.plugins[one_plugin.name] = one_plugin
        self.inited = True

    async def load_plugins(self, group_id: int):
        """
        给某个群加载默认插件
        """
        self.init()
        for module_name, plugin in self.plugins.items():
            flag = await PluginInfo.check_inited(group_id, module_name)
            if flag:
                continue
            metadata = plugin.metadata
            config: PluginConfig = metadata.config
            await PluginInfo.init_plugin(
                group_id=group_id,
                module_name=module_name,
                status=config.default_status,
            )

    def get_module_name(self, plugin_name: str) -> Optional[str]:
        """
        说明:
            获取插件名称对应的模块名称

        参数:
            * `plugin_name`: 插件名称

        返回:
            * `str`: 模块名称
        """
        self.init()
        for module_name, plugin in self.plugins.items():
            if plugin_name == plugin.metadata.name:
                return module_name
        return None

    async def get_group_plugin_status(self, group_id: int) -> list[dict]:
        """
        说明:
            获取某个群的插件状态

        参数:
            * `group_id`：群号

        返回:
            * `list[dict]`：插件相关内容
        """

        self.init()
        plugin_data = await PluginInfo.get_group_plugin_status(group_id)
        plugin_list = []
        for one in plugin_data:
            plugin = self.plugins.get(one["module_name"])
            if plugin is None:
                continue
            config: PluginConfig = plugin.metadata.config
            one_data = {
                "plugin_name": plugin.metadata.name,
                "usage": plugin.metadata.usage,
                "description": plugin.metadata.description,
                "cost_gold": config.cost_gold if config.cost_gold != 0 else "-",
                "status": one["status"],
            }
            plugin_list.append(one_data)
        return plugin_list


plugin_manager = PluginManager()
"""
插件管理器实例
"""
