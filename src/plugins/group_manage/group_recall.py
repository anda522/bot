# python3
# -*- coding: utf-8 -*-
import json

from nonebot import on_notice
from nonebot.adapters.onebot.v11 import NoticeEvent, Bot

from .config import global_config

su = global_config.superusers


async def _group_recall(bot: Bot, event: NoticeEvent) -> bool:
    # 有需要自行取消注释
    if event.notice_type == 'group_recall':
        return True
    return False


group_recall = on_notice(_group_recall, priority=5)


@group_recall.handle()
async def _(bot: Bot, event: NoticeEvent):
    event_obj = json.loads(event.json())
    user_id = event_obj['user_id']  # 消息发送者
    operator_id = event_obj['operator_id']  # 撤回消息的人
    group_id = event_obj['group_id']  # 群号
    message_id = event_obj['message_id']  # 消息 id

    if int(user_id) != int(operator_id): return  # 撤回人不是发消息人，是管理员撤回成员消息，不处理
    if int(operator_id) in su or str(operator_id) in su: return  # 发起撤回的人是超管，不处理
    # 管理员撤回自己的也不处理
    operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id, no_cache=True)
    if operator_info['role'] != 'member': return
    # 防撤回
    recalled_message = await bot.get_msg(message_id=message_id)
    recall_notice = f"检测到{operator_info['card'] if operator_info['card'] else operator_info['nickname']}({operator_info['user_id']})撤回了一条消息：\n\n"
    await bot.send_group_msg(group_id=group_id, message=recall_notice + recalled_message['message'])

