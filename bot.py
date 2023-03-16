#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot import V11Adapter

# Custom your logger
from nonebot.log import logger, default_format
from datetime import datetime
# 出错时将错误信息加入错误日志
logger.add("./logs/{0}H Error.log".format(datetime.strftime(datetime.now(), "%Y-%m-%d %H")),
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

# 定时器自动开始
nonebot.init(apscheduler_autostart=True)
app = nonebot.get_asgi()

# 获取驱动器
driver = nonebot.get_driver()
# 注册协议适配器
driver.register_adapter(
    adapter=V11Adapter
)

# 加载内置插件
nonebot.load_builtin_plugins("echo")
# 加载插件/plugins目录
# nonebot.load_plugins("src/plugins")
# 加载单个插件
nonebot.load_plugin("src.plugins.group_manage")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
