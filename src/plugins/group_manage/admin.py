# python3
# -*- coding: utf-8 -*-
import asyncio
from random import randint
from traceback import print_exc

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .config import global_config, plugin_config
from .utils import At, MsgText, banSb, change_s_title, fi, log_fi, sd, Reply, log_sd, json_load, json_upload

su = global_config.superusers

ban = on_command('禁', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@ban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /禁 @user 禁言
    """
    try:
        msg = MsgText(event.json()).replace(' ', '').replace('禁', '')
        time = int(''.join(map(str, list(map(lambda x: int(x), filter(lambda x: x.isdigit(), msg))))))
        # 提取消息中所有数字作为禁言时间
    except ValueError:
        time = None
    sb = At(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=time)
        try:
            async for baned in baning:
                if baned:
                    await baned
            await log_fi(matcher, '禁言操作成功' if time is not None else '用户已被禁言随机时')
        except ActionFailed:
            await fi(matcher, '权限不足')


unban = on_command('解', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@unban.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /解 @user 解禁
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        baning = banSb(gid, ban_list=sb, time=0)
        try:
            async for baned in baning:
                if baned:
                    await baned
            await log_fi(matcher, '解禁操作成功')
        except ActionFailed:
            await fi(matcher, '权限不足')


ban_all = on_command('/all', aliases={'/全员'}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1,
                     block=True)


@ban_all.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    # note: 如果在 .env.* 文件内设置了 COMMAND_START ，且不包含 "" (即所有指令都有前缀，假设 '/' 是其中一个前缀)，则应该发 //all 触发
    /all 全员禁言
    /all  解 关闭全员禁言
    """
    msg = event.get_message()
    if msg and '解' in str(msg):
        enable = False
    else:
        enable = True
    try:
        await bot.set_group_whole_ban(
            group_id=event.group_id,
            enable=enable
        )
        await log_fi(matcher, f"全体操作成功: {'禁言' if enable else '解禁'}")
    except ActionFailed:
        await fi(matcher, '权限不足')


change = on_command('改', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@change.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /改 @user xxx 改群昵称
    """
    msg = str(event.get_message())
    logger.info(msg.split())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        try:
            for user_ in sb:
                await bot.set_group_card(
                    group_id=gid,
                    user_id=int(user_),
                    card=msg.split()[-1:][0]
                )
            await log_fi(matcher, '改名片操作成功')
        except ActionFailed:
            await fi(matcher, '权限不足')


title = on_command('头衔', priority=1, block=True)


@title.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /头衔 @user  xxx  给某人头衔
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    s_title = msg.replace(' ', '').replace('头衔', '', 1)
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id
    if not sb or (len(sb) == 1 and sb[0] == uid):
        await change_s_title(bot, matcher, gid, uid, s_title)
    elif sb:
        if 'all' not in sb:
            if uid in su or (str(uid) in su):
                for qq in sb:
                    await change_s_title(bot, matcher, gid, int(qq), s_title)
            else:
                await fi(matcher, '超级用户才可以更改他人头衔，更改自己头衔请直接使用【头衔 xxx】')
        else:
            await fi(matcher, '不能含有@全体成员')


title_ = on_command('删头衔', priority=1, block=True)


@title_.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /删头衔 @user 删除头衔
    """
    s_title = ''
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id
    if not sb or (len(sb) == 1 and sb[0] == uid):
        await change_s_title(bot, matcher, gid, uid, s_title)
    elif sb:
        if 'all' not in sb:
            if uid in su or (str(uid) in su):
                for qq in sb:
                    await change_s_title(bot, matcher, gid, int(qq), s_title)
            else:
                await fi(matcher, '超级用户才可以删他人头衔，删除自己头衔请直接使用【删头衔】')
        else:
            await fi(matcher, '不能含有@全体成员')


kick = on_command('踢', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@kick.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    """
    /踢 @user 踢出某人
    """
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if 'all' not in sb:
            try:
                for qq in sb:
                    if qq == event.user_id:
                        await sd(matcher, '你在玩一种很新的东西，不能踢自己!')
                        continue
                    if qq in su or (str(qq) in su):
                        await sd(matcher, '超级用户不能被踢')
                        continue
                    await bot.set_group_kick(
                        group_id=gid,
                        user_id=int(qq),
                        reject_add_request=False  # 还可再接受加群请求
                    )
                await log_fi(matcher, '踢人操作执行完毕')
            except ActionFailed:
                await fi(matcher, '权限不足')
        await fi(matcher, '不能含有@全体成员')


black = on_command('黑', aliases={'拉黑'}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@black.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent, state: T_State):
    """
    黑 @user 拉黑某人 然后踢出
    """
    # 检查at了谁，并不检查qq号
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id

    if sb and 'all' in sb:
        await fi(matcher, '不能含有@全体成员')
    if not sb:
        sb = str(state['_prefix']['command_arg']).split(' ')

    try:
        for qq in sb:
            if qq == event.user_id:
                await sd(matcher, '不能拉黑自己!')
                continue
            if qq in su or (str(qq) in su):
                await sd(matcher, '超级用户不能被黑')
                continue
            # 添加黑名单并更新数据
            black_list = json_load(plugin_config.black_list_path)
            if not black_list.get(str(gid)):
                black_list[str(gid)] = []
            black_list[str(gid)].append(qq)
            json_upload(plugin_config.black_list_path, black_list)
            # 踢出操作
            await bot.set_group_kick(
                group_id=gid,
                user_id=int(qq),
            )
        await log_fi(matcher, '拉黑操作执行完毕，已将其踢出')
    except ActionFailed:
        await fi(matcher, '权限不足')


unblack = on_command('移除黑名单', aliases={'除黑', '移出黑名单'}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                      priority=1, block=True)


@unblack.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent, state: T_State):
    """
    移除黑名单 @user 将某人移出黑名单
    """
    sb = At(event.json())
    gid = event.group_id
    uid = event.user_id

    if sb and 'all' in sb:
        await fi(matcher, '不能含有@全体成员')
    if not sb:
        sb = str(state['_prefix']['command_arg']).split(' ')

    try:
        for qq in sb:
            qq = int(qq)
            if qq == event.user_id:
                await sd(matcher, '不能移出自己!')
                continue
            if qq in su or (str(qq) in su):
                await sd(matcher, '超级用户不能被操作')
                continue
            try:
                # 移除黑名单并更新数据
                black_list = json_load(plugin_config.black_list_path)
                black_list[str(gid)].remove(qq)
                json_upload(plugin_config.black_list_path, black_list)
            except ValueError:
                await fi(matcher, f'黑名单无此人')
        await log_fi(matcher, '移出黑名单操作执行完毕')
    except ActionFailed:
        await fi(matcher, '权限不足')


get_black_list = on_command('查看黑名单', aliases={'黑名单人员'}, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
                            priority=1, block=True)


@get_black_list.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    black_list = json_load(plugin_config.black_list_path)
    gid = event.group_id
    if not black_list[str(gid)]:
        await matcher.finish("本群黑名单为空")
    msg = ""
    for user in black_list[str(gid)]:
        msg += str(user) + "\n"
    await matcher.finish(msg)


set_essence = on_command("加精", aliases={'加精', 'set_essence'}, priority=5, block=True)


@set_essence.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    rp = Reply(event.json())
    if rp:
        msg_id = rp['message_id']
        await bot.call_api(api='set_essence_msg', message_id=msg_id)


del_essence = on_command("取消精华", aliases={'取消加精', 'del_essence'}, priority=5, block=True)


@del_essence.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    rp = Reply(event.json())
    if rp:
        msg_id = rp['message_id']
        await bot.call_api(api='delete_essence_msg', message_id=msg_id)


msg_recall = on_command('撤回', priority=1, aliases={'recall'}, block=True,
                        permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@msg_recall.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):  # by: @tom-snow
    """
    指令格式:
    /撤回 @user n
    回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。
    不输入 n 则默认 n = 5
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    sb = At(event.json())
    rp = Reply(event.json())
    gid = event.group_id
    recall_msg_id = []
    if rp:
        recall_msg_id.append(rp['message_id'])
    elif sb:
        seq = None
        if len(msg.split(' ')) > 1:
            try:  # counts = n
                counts = int(msg.split(' ')[-1])
            except ValueError:
                counts = 5  # 出现错误就默认为 5 【理论上除非是 /撤回 @user n 且 n 不是数值时才有可能触发】
        else:
            counts = 5

        try:
            for _ in range(counts):  # 获取 n 次
                await asyncio.sleep(randint(0, 5))  # 睡眠随机时间，避免黑号
                res = await bot.call_api('get_group_msg_history', group_id=gid, message_seq=seq)  # 获取历史消息
                flag = True
                for message in res['messages']:  # 历史消息列表
                    if flag:
                        seq = int(message['message_seq']) - 1
                        flag = False
                    if int(message['user_id']) in sb:  # 将消息id加入列表
                        recall_msg_id.append(int(message['message_id']))
        except ActionFailed as e:
            await log_sd(matcher, '获取群历史消息时发生错误', f"获取群历史消息时发生错误：{e}, seq: {seq}", err=True)
            print_exc()
    else:
        await fi(matcher,
                 '指令格式：\n/撤回 @user n\n回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。\n不输入 n 则默认 n = 5')

    # 实际进行撤回的部分
    if recall_msg_id:
        try:
            for msg_id in recall_msg_id:
                await asyncio.sleep(randint(0, 2))  # 睡眠随机时间，避免黑号
                await bot.delete_msg(message_id=msg_id)
            await log_fi(matcher, f"操作成功，一共撤回了 {len(recall_msg_id)} 条消息")
        except ActionFailed as e:
            await log_fi(matcher, '撤回失败', f"撤回失败 {e}")
    else:
        pass
