from nonebot import on_command, on_notice, on_message, on_fullmatch
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import NoticeEvent, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot import require
from .utils import random_sentence, now_time, random_color
from nonebot import get_bot

import json
import random
import datetime
from .file import read


data_path = "./data"
group_path = data_path + "/group"

# require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

tot = dict()

matcher = on_command(
    "帮助",
    aliases={'help'},
    priority=1,
    block=False
)
@matcher.handle()
async def learn():
    time = now_time() + "\n"
    path = group_path + "/welcome.txt"
    msg = time + read(path)
    await matcher.send(msg)

ans000 = on_fullmatch('000', priority=1, block=True)
@ans000.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/000"
    msg = ms.at(uid) + read(path)
    await ans000.finish(msg)

ans001 = on_fullmatch('001', priority=1, block=True)
@ans001.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/001"
    msg = ms.at(uid) + read(path)
    await ans001.finish(msg)

ans010 = on_fullmatch('010', priority=1, block=True)
@ans010.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/010"
    msg = ms.at(uid) + read(path)
    await ans010.finish(msg)

ans011 = on_fullmatch('011', priority=1, block=True)
@ans011.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/011"
    msg = ms.at(uid) + read(path)
    await ans011.finish(msg)

ans100 = on_fullmatch('100', priority=1, block=True)
@ans100.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/100"
    msg = ms.at(uid) + read(path)
    await ans100.finish(msg)

ans101 = on_fullmatch('101', priority=1, block=True)
@ans101.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/101"
    msg = ms.at(uid) + read(path)
    await ans101.finish(msg)

ans110 = on_fullmatch('110', priority=1, block=True)
@ans110.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/110"
    msg = ms.at(uid) + read(path)
    await ans110.finish(msg)

ans111 = on_fullmatch('111', priority=1, block=True)
@ans111.handle()
async def _(event: GroupMessageEvent):
    uid = event.user_id
    path = group_path + "/111"
    msg = ms.at(uid) + read(path)
    sentence = await random_sentence()
    await ans111.finish(msg + sentence)

msg_check = on_message(priority=1, block=False)
@msg_check.handle()
async def _(event: MessageEvent):
    uid = event.user_id
    msg = event.message
    if str(uid) in tot:
        if str(msg) == tot[str(uid)]:
            tot.pop(str(uid))
            scheduler.remove_job(job_id=str(uid))
            msg = ms.at(uid) + "欢迎加入计算机学术交流协会!\n因本群消息过多，可将本群设置为免打扰。\n发送 help 或者 头像表情包 有惊喜哦。"
            await msg_check.finish(msg)

async def kick_off(bot: Bot, uid, gid):
    await bot.set_group_kick(
        group_id=gid,
        user_id=uid,
        reject_add_request=False
    )
    tot.pop(str(uid))

group_check = on_notice(priority=1)
@group_check.handle()
async def _(bot: Bot, event: NoticeEvent):
    if event.notice_type == "group_increase":
        uid = event.user_id
        gid = event.group_id
        random_id = random.randint(1000, 9999)
        msg = ms.at(uid) + "\n请在30秒内在群内发送验证码: " + str(random_id) + " 进行加群验证, 否则会将您请出群聊,误踢请重进!\n赠语:\n"
        sentence = (await random_sentence())
        msg += sentence
        # await bot.call_api("send_group_msg", group_id=gid, message=msg)
        await bot.send_group_msg(group_id=gid, message=msg)
        scheduler.add_job(kick_off, args=(bot, uid, gid), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=30), id=str(uid))
        tot[str(uid)] = str(random_id)


# 每5秒修改一次群名片
@scheduler.scheduled_job("interval", seconds=5)
async def modify_group_card():
    try:
        bot = get_bot()
        # 获取成员信息
        # info = (await bot.call_api("get_group_member_info", **{'group_id': 477853587, 'user_id': 1073355443}))
        # card = info['card']
        # new_card = random_color() + card
        await bot.call_api("set_group_card", **{'group_id': 477853587, 'user_id': 2579272746, 'card': now_time()})
    except(ValueError):
        pass
