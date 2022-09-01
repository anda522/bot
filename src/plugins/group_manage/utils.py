import json
import httpx
from datetime import datetime
from random import randint
from typing import Union
# 随机一言 中 + 英

async def random_sentence() -> str:
    # url = 'http://acgapi.top/API/acgyiyan.php'
    url = 'http://api.tianapi.com/everyday/index?key=1a9119df12425524dfa54b755e74bb86&rand=0'
    try:
        async with httpx.AsyncClient() as client:
            res = (await client.get(url)).read()
        newslist = json.loads(res)['newslist'][0]
        english = newslist['content']
        chinese = newslist['note']
        mes = chinese + '\n' + english
    except Exception as e:
        mes = ''
    return str(mes)

def now_time() -> str:
    time = datetime.now()
    strtime = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
    return strtime

def At(data: str):
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(int(msg["data"]["qq"]))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []

def Reply(data: str):
    """
    检测回复哪条消息，返回 reply 对象
    如果没有回复任何人，返回 None
    :param data: event.json()
    :return: dict | None
    """
    try:
        data = json.loads(data)
        if data["reply"] and data["reply"]["message_id"]:  # 待优化
            return data["reply"]
        else:
            return None
    except KeyError:
        return None

def MsgText(data: str):
    """
    返回消息文本段内容(即去除 cq 码后的内容)
    :param data: event.json()
    :return: str
    """
    try:
        data = json.loads(data)
        # 过滤出类型为 text 的【并且过滤内容为空的】
        msg_text_list = filter(lambda x: x["type"] == "text" and x["data"]["text"].replace(" ", "") != "",
                               data["message"])
        # 拼接成字符串并且去除两端空格
        msg_text = " ".join(map(lambda x: x["data"]["text"].strip(), msg_text_list)).strip()
        return msg_text
    except:
        return ""