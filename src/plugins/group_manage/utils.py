import json
import httpx
from datetime import datetime
from random import randint
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

def random_color() -> str:
    # 潮流,朝夕,粉黛,夜空,晚秋,糖果缤纷,盛夏,日出,霓虹闪烁,马卡龙,科技感,黄昏,高级灰,冬梅,初春,红色
    color = ['<%ĀĀ␇Þ>', '<%ĀĀ␇Ý>', '<%ĀĀ␇Ü>', '<%ĀĀ␇Û>', '<%ĀĀ␇Ú>', '<%ĀĀ␇Ù>',
             '<%ĀĀ␇Ø>', '<%ĀĀ␇×>', '<%ĀĀ␇Ö>', '<%ĀĀ␇Õ>', '<%ĀĀ␇Ô>', '<%ĀĀ␇Ù>',
             '<%ĀĀ␇Ù>', '<%ĀĀ␇Ù>', '<%ĀĀ␇Ù>', '<&ÿÿ5@>']
    color_size = len(color)
    id = randint(0, color_size - 1)
    return color[id]

if __name__ == '__main__':
    print(random_color())