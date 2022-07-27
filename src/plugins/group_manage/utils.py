import json
import httpx
from datetime import datetime

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

