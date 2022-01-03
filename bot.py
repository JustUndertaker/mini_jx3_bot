#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from src.utils.database import database_init
from src.utils.moinkeypath import monkeypatch
from src.utils.scheduler import start_scheduler

# 猴子补丁，针对windows平台，更换事件循环
monkeypatch()
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# 开启数据库
driver.on_startup(database_init)
# 开启定时器
driver.on_startup(start_scheduler)

# 加载管理插件
nonebot.load_plugins("src/managers")
# 加载其他插件
nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    nonebot.logger.warning("建议使用指令[nb run]来运行此项目!")
    nonebot.run(app="__mp_main__:app")
