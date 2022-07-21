## 在plugins下创建新的插件
你的插件只需要在``src/plugins/``下创建新的文件夹即可，插件会自动导入。
::: tip 注意插件名称
nb2中“_”开头的插件不会被导入，请不要创建这种插件，或者选择手动导入。
:::
::: warning 安装nb2商店插件
由于插件管理器的缘故，nb2商店安装的插件将无法适用于此插件管理器，意思是你无法通过指令开关该插件，并且菜单中无法显示；同时，由于项目没有``pyproject.toml``你在商店安装的插件需要手动加载，你需要在``bot.py``25行后加入：
```python
nonebot.load_plugin("商店插件名称")
```
如果想要适配本项目，推荐使用git下载到本地，然后放入``src/plugins``下，手动添加插件元数据。
或者在``site-packages``的插件目录下手动添加（误入歧途
:::
## 使用插件元数据
nb2在beta4中加入了插件元数据，这非常好，请在插件文件夹下的``__init__.py``中加入：
```python
from nonebot.plugin import PluginMetadata

from src.params import PluginConfig

__plugin_meta__ = PluginMetadata(
    name="插件名称",
    description="插件描述",
    usage="使用命令",
    config=PluginConfig(),
)
```
::: danger 在params导入PluginConfig
PluginConfig是本项目自带的插件管理器所需要的配置，如果没有此设置，插件管理器将无法管理此插件。
:::
可以在``src/params.py``找到``PluginConfig``：
```python
class PluginConfig(BaseModel):
    enable_managed: bool = True
    """
    是否受插件管理器管理，若设置成False，插件管理器将不会管理
    """
    default_status: bool = True
    """默认开关"""
    cost_gold: int = 0
    """
    使用花费，这里只是显示在菜单中，真正起效在params的cost_gold()
    """
```
里面字段都有默认设置，如果你想修改该设置，可以使用以下方法：
```python
__plugin_meta__ = PluginMetadata(
    name="插件名称",
    description="插件描述",
    usage="使用命令",
    config=PluginConfig(default_status=False),
)
# 此插件默认开关为关闭
```
## 使用金币工具
如果你想让你的插件每次被调用都会扣掉金币，则可以参考以下方法：
```python
from src.params import cost_gold

matcher = on_xxx() # 定义你的matcher

@matcher.handle(parameterless=[cost_gold(gold=10)]) # 这里的gold就是价格
async def _():
    # 你的响应器
```
::: warning 修改菜单价格
上面的是实际需要消耗的金币，同时你应该修改菜单上显示的价格，你需要：
```python
__plugin_meta__ = PluginMetadata(
    name="插件名称",
    description="插件说明",
    usage="指令",
    config=PluginConfig(cost_gold=10),  # 这里在菜单显示
)
```
:::
## 插件编写
插件如何编写请参考Nonebot2的手册：[文档](https://v2.nonebot.dev/docs/tutorial/plugin/introduction)
::: tip 编写插件乐趣
完成自己写的插件是非常快乐的事，相信我！
:::
