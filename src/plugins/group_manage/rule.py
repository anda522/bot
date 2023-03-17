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


# TODO:之后可以在此文件定义不同的权限角色
# 检测发送信息的qq是否是分群管理
async def _group_sub_admin(event: GroupMessageEvent) -> bool:
    uid = event.sender.user_id
    sub_admins = await approve.get_sub_admins()
    gid = event.group_id
    try:
        qq_list = sub_admins[str(gid)]
        if uid in qq_list:
            return True
    except KeyError:
        return False

"""匹配群子管理消息类型"""
GROUP_SUB_ADMIN: Permission = Permission(_group_sub_admin)


