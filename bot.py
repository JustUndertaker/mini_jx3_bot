#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from src.utils.database import database_init
from src.utils.monkeypatch import monkeypatch
from src.utils.scheduler import start_scheduler

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# 注册数据库
driver.on_startup(database_init)
# 开启定时器
driver.on_startup(start_scheduler)

# 加载管理插件
nonebot.load_plugins("src/managers")
# 加载其他插件
nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    monkeypatch()  # 猴子补丁，针对windows平台，更换事件循环
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
