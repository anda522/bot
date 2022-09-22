from nonebot import on_command, on_notice, on_message, on_fullmatch, logger
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import NoticeEvent, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.onebot.v11 import GROUP
from nonebot.exception import ActionFailed
from nonebot.permission import SUPERUSER
from .utils import random_sentence, now_time, At, Reply, MsgText
from nonebot import get_bot
from pathlib import Path
from asyncio import sleep as asleep
from random import randint
from traceback import print_exc

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
            msg = ms.at(uid) + "欢迎加入计算机学术交流协会!\n因本群消息过多，可将本群设置为免打扰。\n发送 help 可查看命令列表。"
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
        second = randint(120, 180)
        msg = ms.at(uid) + "\n请在" + str(second) + "秒内在群内发送验证码: " + str(random_id) + " 进行加群验证, 否则会将您请出群聊。\n！！！误踢请重进！！！\n赠语:\n"
        sentence = (await random_sentence())
        msg += sentence
        # await bot.call_api("send_group_msg", group_id=gid, message=msg)
        await bot.send_group_msg(group_id=gid, message=msg)
        scheduler.add_job(kick_off, args=(bot, uid, gid), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=second), id=str(uid))
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


daka = on_command("打卡", aliases={'daka', 'kada', '卡打'}, priority=8)
@daka.handle()
async def _():
    lst = ["daka.jpg", "invdaka.jpg"]
    rnd = random.randint(0, 1)
    path: Path = Path().cwd() / "data" / "group" / lst[rnd]
    msg = ms.text("现在是" + now_time() + ",尽快打卡哦^_^\n") + ms.image(path)
    await daka.finish(msg, at_sender=True)

kick = on_command('乌鸦坐飞机', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)

@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    踢人
    """
    msg = str(event.get_message())
    sb = At(event.json())
    gid = event.group_id
    if sb:
        if 'all' not in sb:
            try:
                for qq in sb:
                    await bot.set_group_kick(
                        group_id=gid,
                        user_id=int(qq),
                        reject_add_request=False
                    )
            except ActionFailed:
                await kick.finish("或许我需要更强的力量")
            else:
                await kick.finish(f"这只乌鸦已成功飞走")
        else:
            await kick.finish("不能含有@全体成员")

msg_recall = on_command("撤回", priority=1, aliases={"删除", "recall"}, block=True,
                        permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)

@msg_recall.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    指令格式:
    /撤回 @user n
    回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。
    不输入 n 则默认 n=3
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    sb = At(event.json())
    rp = Reply(event.json())
    gid = event.group_id

    recall_msg_id = []
    if rp:
        recall_msg_id.append(rp["message_id"])
    elif sb:
        seq = None
        if len(msg.split(" ")) > 1:
            try:  # counts = n
                counts = int(msg.split(" ")[-1])
            except ValueError:
                counts = 3  # 出现错误就默认为 3 【理论上除非是 /撤回 @user n 且 n 不是数值时才有可能触发】
        else:
            counts = 3

        try:
            for i in range(counts):  # 获取 n 次
                await asleep(randint(0, 10))  # 睡眠随机时间，避免黑号
                res = await bot.call_api("get_group_msg_history", group_id=gid, message_seq=seq)  # 获取历史消息
                flag = True
                for message in res["messages"]:  # 历史消息列表
                    if flag:
                        seq = int(message["message_seq"]) - 1
                        flag = False
                    if int(message["user_id"]) in sb:  # 将消息id加入列表
                        recall_msg_id.append(int(message["message_id"]))
        except ActionFailed as e:
            await msg_recall.send(f"获取群历史消息时发生错误")
            logger.error(f"获取群历史消息时发生错误：{e}, seq: {seq}")
            print_exc()
    else:
        await msg_recall.finish("指令格式：\n撤回 @user n\n回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。\n不输入 n 则默认 n=3")

    # 实际进行撤回的部分
    try:
        for msg_id in recall_msg_id:
            await asleep(randint(0, 3))  # 睡眠随机时间，避免黑号
            await bot.call_api("delete_msg", message_id=msg_id)
    except ActionFailed as e:
        logger.warning(f"执行失败，可能是我权限不足 {e}")
        await msg_recall.finish("执行失败，可能是我权限不足")
    else:
        logger.info(f"操作成功，一共撤回了 {len(recall_msg_id)} 条消息")
        await msg_recall.finish(f"操作成功，一共撤回了 {len(recall_msg_id)} 条消息")

