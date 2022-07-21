## 声明
本机器人使用[Nonebot2](https://github.com/nonebot/nonebot2)框架，需要掌握一定程度的python能力，如果纯小白的话建议先学python：[文档](https://docs.python.org/zh-cn/3/)

## 项目结构
当前项目结构如下：
```tree
📦mini_jx3_bot
 ┣ 📂data         # 运行数据目录
 ┣ 📂docs         # 文档
 ┣ 📂log          # 运行日志目录
 ┃ ┣ 📂debug
 ┃ ┣ 📂error
 ┃ ┗ 📂info
 ┣ 📂src          # 代码目录
 ┃ ┣ 📂managers   # 管理插件
 ┃ ┣ 📂modules    # 数据库表
 ┃ ┣ 📂plugins    # 自定义插件
 ┃ ┗ 📂utils      # 工具模块
 ┣ 📂template     # 渲染模板目录
 ┣ 📜.env.prod    # 项目环境文件
 ┣ 📜bot.py       # 项目入口
 ┣ 📜config.yml   # 项目配置文件
 ┗ 📜requirements.txt   # 项目依赖
```
