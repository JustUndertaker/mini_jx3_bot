## 配置文件
::: tip 设置
本项目兼容使用Nonebot2的配置``.env``文件，使用``key = value``配置，你可以自由添加
:::
如果你想在代码中获取你的配置：
```python
from nonebot import get_driver

config = get_driver().config
value = config['你的配置key']
```
::: tip pydantic
如果想获得配置提示，请使用pydantic模型：[文档](https://pydantic-docs.helpmanual.io/)
:::
你可以参考``src/config.py``：
```python
from pydantic import BaseModel, Extra, Field

class NlpConfig(BaseModel, extra=Extra.ignore):
    """
    nlp配置
    """

    secretId: str = Field("", alias="nlp_secretId")
    secretKey: str = Field("", alias="nlp_secretKey")

# 创建配置实例
config = get_driver().config
nlp_config = NlpConfig.parse_obj(config)
```
你可以将上述class改成你需要的配置，记得在``.env``文件下加入你的key。

## 日志工具
::: tip loguru
本项目日志使用loguru：[文档](https://loguru.readthedocs.io/en/stable/index.html)
:::
同时本项目自己新建了记录器，默认支持颜色标签，如果你想让你的日志保存在``logs``文件夹下，可以导入使用：
```python
from src.utils.log import logger

logger.info("你的日志信息")
```
## 定时器工具
::: tip Apscheduler
本项目定时器使用Apscheduler：[文档](https://apscheduler.readthedocs.io/en/master/?badge=latest)
:::
本项目自定义了一个管理器，如果需要使用，请参考以下办法：
```python
from src.utils.scheduler import scheduler

@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    # 每天0点运行此函数
```
## 浏览器工具
::: tip playwright
本项目浏览器使用playwright：[文档](https://playwright.dev/python/)
:::
使用浏览器可以通过模板语法生成html页面，然后截图发送给用户，项目封装了browser工具用于截图，你可以这样使用：
```python
from src.utils.browser import browser

async def fun():
    img_bytes=await browser.template_to_image(
        pagename=pagename,
        **kwargs
    )
```
其中``pagename``是你的模板文件名，它应该是位于``template``文件夹下的模板文件，``kwargs``是你要注入到模板内的数据，使用关键字参数传递。
::: tip jinja2
本项目使用jinja2模板：[文档](http://doc.yonyoucloud.com/doc/jinja2-docs-cn/index.html)
:::
::: tip 相对引用
特别地，本项目将模板的根目录定位在了``template``下，如果你想在模板文件下使用外部文件，可以相对此目录引用：
```html
<link rel="stylesheet" href="./css/bootstrap.min.css">
```
:::
## 使用数据库
::: tip Tortoise-orm
本项目使用sqlite作为数据库，同时orm选用Tortoise-orm：[文档](https://tortoise.github.io/)
:::
表模型存放在``src/modules``下：
```tree
📂modules
 ┣ 📜group_info.py      # 群信息
 ┣ 📜plugin_info.py     # 插件开关信息
 ┣ 📜search_record.py   # 查询记录信息
 ┣ 📜ticket_info.py     # 推栏ticket信息
 ┗ 📜user_info.py       # 用户信息
```
在需要的时候import下来即可使用：
```python
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.modules.search_record import SearchRecord
from src.modules.ticket_info import TicketInfo
from src.modules.user_info import UserInfo
```
::: tip 表接口
每个表都内置实现了部分接口，都是@classmethod，不需要创建实例直接调用即可，你可以在对应的module下自定义新的接口，建议同样使用@classmethod
:::
::: warning 定义新表
如果你想定义新的表，除了在``src/modules``下创建新的模型外，还需要在``src/internal/database.py``引入你的module：
```python
# 这里填要加载的表
    models = [
        "src.modules.group_info",
        "src.modules.plugin_info",
        "src.modules.user_info",
        "src.modules.ticket_info",
        "src.modules.search_record",
    ]
```
:::
