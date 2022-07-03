from nonebot import on_command, on_notice, on_message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import NoticeEvent, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot import require


import json
import random
import datetime
from .file import read

PATH = "../../../data/group"

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

tot = dict()

matcher = on_command(
    "计协",
    aliases={'/jixie'}
)

@matcher.handle()
async def learn():
    await matcher.send("Hello World")


msg_check = on_message()
@msg_check.handle()
async def _(event: MessageEvent):
    uid = event.user_id
    msg = event.message
    if str(uid) in tot:
        if str(msg) == tot[str(uid)]:
            tot.pop(str(uid))
            scheduler.remove_job(job_id=str(uid))
            msg = ms.at(uid) + "欢迎加入计算机学术交流协会!"
            await msg_check.finish(msg)

async def kick_off(bot: Bot, uid, gid):
    await bot.set_group_kick(
        group_id=gid,
        user_id=uid,
        reject_add_request=False
    )
    tot.pop(str(uid))

group_check = on_notice(priority=2)
@group_check.handle()
async def _(bot: Bot, event: NoticeEvent):
    if event.notice_type == "group_increase":
        uid = event.user_id
        gid = event.group_id
        random_id = random.randint(1000, 9999)
        msg = ms.at(uid) + "\n请在30秒内发送验证码: " + str(random_id) + " 进行加群验证, 否则会将您请出群聊, 谢谢配合!"
        # await bot.call_api("send_group_msg", group_id=gid, message=msg)
        await bot.send_group_msg(group_id=gid, message=msg)
        scheduler.add_job(kick_off, args=(bot, uid, gid), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=30), id=str(uid))
        tot[str(uid)] = str(random_id)
