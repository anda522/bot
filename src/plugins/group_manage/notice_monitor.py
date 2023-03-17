# python3
# -*- coding: utf-8 -*-
import asyncio
import random
import datetime

from nonebot.adapters.onebot.v11 import (
    Bot, Event, PokeNotifyEvent,
    MessageEvent,
    HonorNotifyEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent,
    MessageSegment
)
from nonebot.matcher import Matcher
from nonebot.plugin import on_notice
from nonebot.typing import T_State
from nonebot import require, on_message
from .config import plugin_config
from .file import read
from .utils import fi, now_time

try:
    scheduler = require('nonebot_plugin_apscheduler').scheduler
except BaseException:
    scheduler = None

wait_verify_list = dict()


# 获取戳一戳状态
async def _is_poke(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()


# 获取群荣誉变更
async def _is_honor(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, HonorNotifyEvent)


# 获取文件上传
async def _is_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupUploadNoticeEvent)


# 群成员减少
async def _is_user_decrease(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupDecreaseNoticeEvent)


# 群成员增加
async def _is_user_increase(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)


# 管理员变动
async def _is_admin_change(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupAdminNoticeEvent)


# 红包运气王
async def _is_red_packet(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, LuckyKingNotifyEvent)


poke = on_notice(_is_poke, priority=50, block=True)
honor = on_notice(_is_honor, priority=50, block=True)
upload_files = on_notice(_is_checker, priority=50, block=True)
user_decrease = on_notice(_is_user_decrease, priority=50, block=True)
user_increase = on_notice(_is_user_increase, priority=50, block=True)
admin_change = on_notice(_is_admin_change, priority=50, block=True)
red_packet = on_notice(_is_red_packet, priority=50, block=True)


@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # TODO 在本地做记录，因为dev分支已经用了数据库，后再在写
    ...


@honor.handle()
async def _(bot: Bot, event: HonorNotifyEvent, state: T_State, matcher: Matcher):
    honor_type = event.honor_type
    gid = event.group_id
    uid = event.user_id
    reply = ""
    honor_map = {"performer": ["🔥", "群聊之火"], "emotion": ["🤣", "快乐源泉"]}
    # 龙王
    u_info = await bot.get_group_member_info(group_id=gid, user_id=event.user_id)
    u_name = u_info["card"] if u_info["card"] else u_info["nickname"]
    if honor_type == "talkative":
        if uid == bot.self_id:
            reply = "💦 新龙王诞生，原来是我自己~"
        else:
            reply = f"💦 恭喜 {u_name} 荣获龙王标识~"
    for key, value in honor_map.items():
        if honor_type == key:
            reply = f"{value[0]} 恭喜{u_name}荣获【{value[1]}】标识~"
    await fi(matcher, reply)


@upload_files.handle()
async def _(bot: Bot, event: GroupUploadNoticeEvent, state: T_State, matcher: Matcher):
    # TODO 在本地做记录
    ...


@user_decrease.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State, matcher: Matcher):
    # op = await bot.get_group_member_info(group_id=event.group_id, user_id=event.operator_id)
    casualty_name = (await bot.get_stranger_info(user_id=event.user_id)).get("nickname")
    # op_name = op['card'] if op.get('card') else op['nickname']
    e_time = now_time()
    avatar = get_avatar(event.user_id)
    farewell_words = "感谢/o给/n送上的飞机，谢谢/o"
    farewell_self_words = "/n离群出走/n"
    # TODO 为以后自定义欢送词做准备
    if event.operator_id != event.user_id:
        reply = f"🛫 成员变动\n {farewell_words.replace('/o', f' {casualty_name} ').replace('/n', f' {casualty_name} ')}"
        reply += MessageSegment.image(avatar) + f" \n {e_time}\n"
    else:
        reply = f"🛫 成员变动\n {farewell_self_words.replace('/n', f' {casualty_name} ')}"
    await fi(matcher, reply)


async def kick_off(bot: Bot, uid, gid):
    await bot.set_group_kick(
        group_id=gid,
        user_id=uid,
        reject_add_request=False
    )
    wait_verify_list.pop(str(uid))


@user_increase.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State, matcher: Matcher):
    gid = event.group_id
    uid = event.user_id
    await asyncio.sleep(1)
    avatar = get_avatar(event.user_id)
    new_be = (await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id))['nickname']
    wel_words = read(plugin_config.welcome_path)
    # 自定义欢迎词
    reply = "✨ 成员变动\n" + MessageSegment.image(avatar) + MessageSegment.at(event.user_id) + "欢迎加入\n" + wel_words
    await bot.send_group_msg(group_id=gid, message=reply)
    random_id = random.randint(1000, 9999)
    time = random.randint(120, 180)
    msg = MessageSegment.at(uid) + "\n请在" + str(time) + "秒内在群内发送验证码: " + str(
        random_id) + " 进行加群验证, 否则会将您请出群聊。\n！！！误踢请重进！！！"
    scheduler.add_job(kick_off, args=(bot, uid, gid),
                      next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=time), id=str(uid))
    wait_verify_list[str(uid)] = str(random_id)
    await fi(matcher, msg)


msg_check = on_message(priority=1, block=False)
@msg_check.handle()
async def _(event: MessageEvent):
    uid = event.user_id
    msg = event.message
    if str(uid) in wait_verify_list:
        if str(msg) == wait_verify_list[str(uid)]:
            wait_verify_list.pop(str(uid))
            scheduler.remove_job(job_id=str(uid))
            msg = MessageSegment.at(uid) + "欢迎加入"
            await msg_check.finish(msg)


@admin_change.handle()
async def _(bot: Bot, event: GroupAdminNoticeEvent, state: T_State, matcher: Matcher):
    reply = ""
    sub_type = event.sub_type
    uid = event.user_id
    user = await bot.get_group_member_info(group_id=event.group_id, user_id=uid)
    u_name = user['card'] if user.get('card') else user['nickname']
    cong_words = "恭喜/n成为管理"
    re_words = "Ops! /n不再是本群管理"
    if uid == bot.self_id:
        if sub_type == "set":
            reply = f"🚔 管理员变动\n{cong_words.replace('/n', '我')}"
        if sub_type == "unset":
            reply = f"🚔 管理员变动\n{re_words.replace('/n', '我')}"
    else:
        if sub_type == "set":
            reply = f"🚔 管理员变动\n{cong_words.replace('/n', f' {u_name} ')}"
        if sub_type == "unset":
            reply = f"🚔  管理员变动\n{re_words.replace('/n', f' {u_name} ')}"
    await fi(matcher, reply)


@red_packet.handle()
async def _(bot: Bot, event: LuckyKingNotifyEvent, state: T_State, matcher: Matcher):
    # TODO 也许做点本记录（运气王）
    ...


def get_avatar(uid):
    return f"https://q4.qlogo.cn/headimg_dl?dst_uin={uid}&spec=640"
