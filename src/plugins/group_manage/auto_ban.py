import re

from nonebot import logger, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from .config import plugin_config
from .utils import del_txt_line, add_txt_line, get_txt_line, banSb, get_user_violation, sd

ban_prohibited_word = on_message(priority=2, block=False)


@ban_prohibited_word.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """
    违禁词禁言
    :param bot:
    :param event:
    :return:
    """
    rules = [re.sub(r'\t+', '\t', rule).split('\t') for rule in
             plugin_config.limit_word_path.read_text(encoding='utf-8').split('\n')]
    msg = re.sub(r'\s', '', str(event.get_message()))
    gid = event.group_id
    uid = event.user_id
    logger.info(f"{gid}收到{uid}的消息: \"{msg}\"")
    for rule in rules:
        if not rule[0]: continue
        delete, ban = True, True  # 默认禁言&撤回
        if len(rule) > 1:
            delete, ban = rule[1].find('$撤回') != -1, rule[1].find('$禁言') != -1
            rf = re.search(r'\$(仅限|排除)(([0-9]{6,},?)+)', rule[1])
            if rf:
                chk = rf.groups()
                lst = chk[1].split(',')
                if chk[0] == '仅限':
                    if str(gid) not in lst:
                        continue
                else:
                    if str(gid) in lst:
                        continue
        try:
            if not re.search(rule[0], msg):
                continue
        except:
            if msg.find(rule[0]) == -1:
                continue
        matcher.stop_propagation()  # block
        level = (await get_user_violation(gid, uid, 'Porn', event.raw_message))
        ts: list = plugin_config.time_scop_map[level]
        logger.info(f"敏感词触发: \"{rule[0]}\"")
        if delete:
            try:
                await bot.delete_msg(message_id=event.message_id)
                logger.info('消息已撤回')
            except ActionFailed:
                logger.info('消息撤回失败')
        if ban:
            baning = banSb(gid, ban_list=[event.get_user_id()], scope=ts)
            async for baned in baning:
                if baned:
                    try:
                        await baned
                        await sd(matcher,
                                 f"你发送了违禁词,现在进行处罚,如有异议请联系管理员\n你的违禁级别为{level}级", True)
                        logger.info(f"禁言成功，用户: {uid}")
                    except ActionFailed:
                        logger.info('禁言失败，权限不足')
        break


cb_notice = plugin_config.callback_notice

del_custom_limit_words = on_command('删除违禁词', aliases={'移除违禁词', '去除违禁词'}, priority=1,
                                    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@del_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    await del_txt_line(plugin_config.limit_word_path, matcher, event, args, '违禁词', False)


# TODO: 支持配置是否撤回&禁言
add_custom_limit_words = on_command('添加违禁词', aliases={'增加违禁词', '新增违禁词'}, priority=1,
                                    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@add_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    await add_txt_line(plugin_config.limit_word_path, matcher, event, args, '违禁词', False)


get_custom_limit_words = on_command('查看违禁词',
                                    aliases={'查看违禁词', '查询违禁词', '违禁词列表'}, priority=1,
                                    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@get_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if cb_notice:
        await get_txt_line(plugin_config.limit_word_path, matcher, event, args, '违禁词', False)