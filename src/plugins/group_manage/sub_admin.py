from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.internal.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from . import approve
from .utils import At, fi
from .func_hook import check_func_status

sub_admin = on_command('子管理', aliases={'查看群管理'}, priority=1, block=True,
                       permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@sub_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    gid = str(event.group_id)
    admins = await approve.get_sub_admins()
    try:
        rely = str(admins[gid])
        await sub_admin.finish(f"本群子管理：{rely}")
    except KeyError:
        await sub_admin.finish('查询不到呢，使用 子管理+ @xx 来添加子管理')


# 查看所有子管理
all_sub_admin = on_command('所有子管理', aliases={'所有分群子管理'}, priority=1, block=True, permission=SUPERUSER)


@all_sub_admin.handle()
async def _(bot: Bot, event: MessageEvent):
    admins = await approve.get_sub_admins()
    await all_sub_admin.finish(str(admins))


# 添加分群管理员
add_sub_admin = on_command('子管理+', aliases={'分群子管理+'}, priority=1, block=True,
                     permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@add_sub_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent, state: T_State):
    sb = At(event.json())
    gid = str(event.group_id)
    if not sb:
        sb = str(state['_prefix']['command_arg']).split(' ')

    if 'all' not in sb:
        for qq in sb:
            g_admin_handle = await approve.add_sub_admins(gid, int(qq))
            if g_admin_handle:
                await add_sub_admin.send(f"{qq}已成为本群分群管理")
            else:
                await add_sub_admin.send(f"用户{qq}已存在")


# 删除分群管理
delete_sub_admin = on_command('子管理-', aliases={'分群管理-'}, priority=1, block=True,
                      permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@delete_sub_admin.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent, state: T_State):
    sb = At(event.json())
    gid = str(event.group_id)
    # TODO:这句话应该没用了，之后要考虑删除
    status = await check_func_status('requests', str(gid))

    if not sb:
        sb = str(state['_prefix']['command_arg']).split(' ')

    if 'all' not in sb:
        for qq in sb:
            g_admin_del_handle = await approve.delete_sub_admins(gid, int(qq))
            if g_admin_del_handle:
                await delete_sub_admin.send(f"{qq}删除成功")
            elif not g_admin_del_handle:
                await delete_sub_admin.send(f"{qq}还不是分群管理")
            elif g_admin_del_handle is None:
                await delete_sub_admin.send(f"群{gid}未添加过分群管理")
