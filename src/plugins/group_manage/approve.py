import json
from typing import Optional
from nonebot import logger

from .utils import json_load
from .config import plugin_config


async def get_sub_admins():
    """
    :return : 分群管理json对象
    """
    with open(plugin_config.config_group_admin, mode='r') as f:
        admins = json.load(f)
    return admins


async def add_sub_admins(gid: str, qq: int) -> Optional[bool]:
    """
    添加分群管理（处理加群请求时接收处理结果）
    :param gid: 群号
    :param qq: qq
    :return: bool
    """
    admins = await get_sub_admins()
    if gid in admins:
        if qq in admins[gid]:
            logger.info(f"{qq}已经是群{gid}的分群管理了")
            return False
        else:
            sub_admins = admins[gid]
            sub_admins.append(qq)
            admins[gid] = sub_admins
            with open(plugin_config.config_group_admin, mode='w') as c:
                c.write(str(json.dumps(admins)))
            logger.info(f"群{gid}添加分群管理：{qq}")
            return True
    else:
        logger.info(f"群{gid}首次加入分群管理")
        admins.update({gid: [qq]})
        with open(plugin_config.config_group_admin, mode='w') as c:
            c.write(str(json.dumps(admins)))
        return True


async def delete_sub_admins(gid: str, qq: int) -> Optional[bool]:
    """
    删除分群管理
    :param gid: 群号
    :param qq: qq
    :return: bool
    """
    admins = await get_sub_admins()
    if gid in admins:
        if qq in admins[gid]:
            logger.info(f"已删除群{gid}的分群管理{qq}")
            data = admins[gid]
            data.remove(qq)
            if data:
                admins[gid] = data
            else:
                del (admins[gid])
            with open(plugin_config.config_group_admin, mode='w') as c:
                c.write(str(json.dumps(admins)))
            return True
        else:
            logger.info(f"删除失败：群{gid}中{qq}还不是分群管理")
            return False
    else:
        logger.info(f"群{gid}还未添加过分群管理")
        return None


async def write(gid: str, answer: str) -> Optional[bool]:
    """
    添加词条
    :param gid: 群号
    :param answer: 词条
    :return: bool
    """
    contents = json_load(plugin_config.config_admin)
    if gid in contents:
        data = contents[gid]
        if answer in data:
            logger.info(f"{answer} 已存在于群{gid}的词条中")
            return False
        else:
            data.append(answer)
            contents[gid] = data
            with open(plugin_config.config_admin, mode='w') as c:
                c.write(str(json.dumps(contents)))
            logger.info(f"群{gid}添加入群审批词条：{answer}")
            return True
    else:
        logger.info(f"群{gid}第一次配置此词条：{answer}")
        contents.update({gid: [answer]})
        with open(plugin_config.config_admin, mode='w') as c:
            c.write(str(json.dumps(contents)))
        return True


async def delete(gid: str, answer: str) -> Optional[bool]:
    """
    删除词条
    :param gid: 群号
    :param answer: 词条
    :return: bool
    """
    contents = json_load(plugin_config.config_admin)
    if gid in contents:
        if answer in contents[gid]:
            data = contents[gid]
            data.remove(answer)
            if data:
                contents[gid] = data
            else:
                del (contents[gid])
            with open(plugin_config.config_admin, mode='w') as c:
                c.write(str(json.dumps(contents)))
            logger.info(f'群{gid}删除词条：{answer}')
            return True

        else:
            logger.info(f"删除失败，群{gid}不存在词条：{answer}")
            return False
    else:
        logger.info(f"群{gid}从未配置过词条")
        return None
