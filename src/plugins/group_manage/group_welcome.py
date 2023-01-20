from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GROUP_ADMIN,
    GROUP_OWNER,
    MessageEvent,
    GroupIncreaseNoticeEvent,
)
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.matcher import Matcher
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot import logger
from .file import write, read
from .config import plugin_config


# 群成员增加
async def _is_user_increase(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)


edit_welcome_txt = on_command('修改欢迎词', aliases={'修改欢迎', '改变欢迎词'}, priority=1, block=True,
                          permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@edit_welcome_txt.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    write(plugin_config.welcome_path, args)
    await matcher.finish()


get_welcome_txt = on_command('查看欢迎词', aliases={'查看欢迎', '欢迎词'}, priority=1, block=True,
                             permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@get_welcome_txt.handle()
async def _():
    msg = read(plugin_config.welcome_path)
    logger.info("欢迎词 已发送")
    await get_welcome_txt.finish(msg)
