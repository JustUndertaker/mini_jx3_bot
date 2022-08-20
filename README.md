<div align="center">

# 团子机器人

_✨基于[nonebot2](https://github.com/nonebot/nonebot2)的剑网三群聊机器人，采用[jx3api](https://jx3api.com)作为数据源。✨_

</div>

<p align="center">
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/python-3.10-blue" alt="license"></a>
<a href="https://github.com/nonebot/nonebot2">
<img src="https://img.shields.io/badge/nonebot-2.0.0b4-yellow"></a>
<a href="https://github.com/Mrs4s/go-cqhttp">
<img src="https://img.shields.io/badge/go--cqhttp-v1.0.0--rc3-red"></a>
</p>


## 这是什么
一个使用gocq作为协议端的QQ群聊机器人，可以接受处理QQ消息并回复，接入了[JX3API](https://www.jx3api.com)的数据后，可以查询《剑网三》内的游戏数据,你可以：
- 自己部署到服务器，创建自己的机器人
- 添加自己写的插件，适配到机器人中

## 文档
传送门：[使用文档](https://justundertaker.github.io/mini_jx3_bot/)
## 鸣谢
- [Onebot](https://onebot.dev/)：简洁、通用、可扩展，只需使用一套标准即可为各种平台编写聊天机器人。
- [Nonebot2](https://github.com/nonebot/nonebot2)：跨平台 Python 异步聊天机器人框架。
- [Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：cqhttp的golang实现，轻量、原生跨平台。
- [JX3API](https://www.jx3api.com)：剑网三游戏数据源。
## 联系我
一个游戏策划，QQ群：776825118


## docker 部署

安装 docker

`docker -v  2> /dev/null|| curl -sSL https://get.daocloud.io/docker | sh`

其中 .env.prod 中的所有环境变量都可以通过 -e 的形式加在容器启动命令中

`docker run --name="mini_jx3_bot" -e superusers=["你的QQ"] -e botname="团子"  -p 8080:8080 -itd ermaozi/mini_jx3_bot`

把数据存在本地防止数据随容器丢失, 同理, 日志目录也可以从本地挂载, 方便日志查看. 日志路径: /mini_jx3_bot/logs

`mkdir ~/data/`

`docker run --name="mini_jx3_bot" -v ~/data:/mini_jx3_bot/data -e superusers=["你的QQ"] -e botname="团子"  -p 8080:8080 -itd ermaozi/mini_jx3_bot`

容器自启动

`docker update --restart=always mini_jx3_bot`

容器自动更新

 `docker run -d --name watchtower --restart always -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup -i 300 mini_jx3_bot`