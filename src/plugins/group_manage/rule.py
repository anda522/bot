"""
定义自定义匹配规则和权限
"""

from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
)
from nonebot.permission import Permission
from . import approve
from .config import plugin_config


# 检测发送信息的qq是否是分群管理
async def user_checker(event: GroupMessageEvent) -> bool:
    uid = event.get_user_id()
    sub_admins = approve.get_sub_admins()
    gid = event.group_id
    try:
        qq_list = sub_admins[str(gid)]
        for qq in qq_list:
            if uid == qq:
                return True
    except ValueError:
        return False
