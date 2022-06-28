from nonebot.plugin import Plugin, get_loaded_plugins
from src.modules.plugin_info import PluginInfo
from src.params import PluginConfig


class PluginManager:
    '''插件管理器'''
    plugins: dict[str, Plugin] = {}
    '''已管理插件映射集'''
    inited: bool = False
    '''是否已初始化'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(PluginManager, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def init(self):
        '''
        初始化加载插件，在第一次使用时需要用到
        '''
        if self.inited:
            return
        loaded_plugins = list(get_loaded_plugins())
        for one_plugin in loaded_plugins:
            # 跳过没有元数据或者配置元数据内不受插件管理器管理的插件
            metadata = one_plugin.metadata
            if metadata is None:
                continue
            config: PluginConfig = metadata.config
            # 判断config是否为None
            if not config:
                continue

            # 判断是否受管理
            if not config.enable_managed:
                continue

            # 储存所有受管理插件
            self.plugins[one_plugin.name] = one_plugin
        self.inited = True

    async def load_plugins(self, group_id: int):
        '''
        给某个群加载默认插件
        '''
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
                plugin_name=metadata.name,
                usage=metadata.usage,
                description=metadata.description,
                status=config.default_status
            )
