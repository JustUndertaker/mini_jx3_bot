#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from src.internal.database import database_init
from src.utils.scheduler import start_scheduler

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 开启数据库
driver.on_startup(database_init)
# 开启定时器
driver.on_startup(start_scheduler)

# 加载管理插件
nonebot.load_plugins("src/managers")
# 加载其他插件
nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    nonebot.logger.warning("请使用指令[nb run]来运行此项目!")
    nonebot.run()
