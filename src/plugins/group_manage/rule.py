"""
定义自定义匹配规则和权限
"""

from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
)


# 检测发送qq是否是分群管理
async def user_checker(event: Event) -> bool:
    for qq in group_admin:
        if qq == Event.user_id():
            return True
