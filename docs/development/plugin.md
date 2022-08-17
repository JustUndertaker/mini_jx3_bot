## 插件编写指南
::: tip 指南
可以参考本项目内置插件编写，也可以参考：[官方文档](https://v2.nonebot.dev/docs/tutorial/plugin/introduction)
:::
## 在plugins下创建新的插件
你的插件只需要在``src/plugins/``下创建新的文件夹即可，插件会自动导入。
::: tip 注意插件名称
nb2中“_”开头的插件不会被导入，请不要创建这种插件，或者选择手动导入。
:::
## 安装nb2插件商店的插件
本项目使用nonebot2框架，支持插件商店安装插件，商店地址：[传送门](https://v2.nonebot.dev/store)
::: danger 元数据
由于本项目的插件管理器使用额外的插件元数据配置管理，商店插件没有此项配置，这将导致：
 - 你无法使用“菜单”命令查看到已加载的该插件
 - 你无法使用“打开/关闭”命令设置该插件开关

如果需要适配插件管理器，可以参考[#添加插件元数据](#添加插件元数据)
:::
### 使用pip或者nb plugin命令安装
::: warning 注意
由于项目不使用``pyproject.toml``管理插件加载，所以使用命令安装插件：
``` bash
nb plugin install plugin_name
```
会提示错误：
``` bash
RuntimeError('Config file .../pyproject.toml does not exist!')
```
忽略此错误，采用手动加载插件。
:::
::: tip 从bot.py加载插件
在bot.py的25行后加入：
``` python
nonebot.load_plugin("商店插件名称")
```
:::
### 使用git安装插件
::: tip 使用git安装插件
可以在github将插件源码下载到本地，插件文件夹放入``src/plugins``下，这样商店插件会当作本地插件自动导入了，不需要额外添加加载插件代码。
:::
## 添加插件元数据
nb2在beta4中加入了插件元数据，本项目插件管理器基于此数据进行插件管理，要使用元数据，需要在插件文件夹下的``__init__.py``中加入：
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
::: tip 对于商店安装的插件
使用pip或者nb plugin安装的商店插件会保存到pip的``site-packages``目录下（对于conda，他应该保存在``conda/envs/evn_name/Lib/site-packages``下），你可以将插件复制到本地插件文件夹下将其变为本地插件，然后添加元数据；也可以直接在此文件夹下修改内容添加元数据（修改后更新插件需要同步修改）
:::
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
