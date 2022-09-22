#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot import V11Adapter

# Custom your logger
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# nonebot.init()
nonebot.init(apscheduler_autostart=True)
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(
    adapter=V11Adapter
)

# 加载内置插件
# nonebot.load_builtin_plugins("echo")
# 加载自定义插件
# nonebot.load_plugins("src/plugins")
# 加载单个插件
# nonebot.load_plugin("src.plugins.bread")
# nonebot.load_plugin("src.plugins.fortune")
nonebot.load_plugin("src.plugins.group_manage")
nonebot.load_plugin("src.plugins.petpet")
nonebot.load_plugin()

if __name__ == "__main__":
    nonebot.run(app="bot:app")
