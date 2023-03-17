import os
import random

import httpx
from wordcloud import WordCloud, ImageColorGenerator
import jieba
from imageio import imread
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from pathlib import Path
from .config import plugin_config
from .utils import participle_simple_handle

cloud = on_command('群词云', priority=1)


@cloud.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    try:
        ttf_name_ = plugin_config.ttf_path
        gid = str(event.group_id)
        path_temp = plugin_config.words_contents_path / f"{gid}.txt"
        dir_list = os.listdir(plugin_config.words_contents_path)
        background_img = os.listdir(plugin_config.wordcloud_bg_path)
        if background_img:
            wordcloud_bg = random.choice(os.listdir(plugin_config.wordcloud_bg_path))
            try:
                async with httpx.AsyncClient() as client:
                    num = int((await client.get(
                        'https://fastly.jsdelivr.net/gh/yzyyz1387/blogimages/nonebot/wordcloud/num.txt')).read())
                    if num > len(background_img):
                        await cloud.send(
                            f"开发者新提供了{num - len(background_img)}张图片，您可以发送【更新mask】下载新的图片")
            except:
                pass

        else:
            try:
                async with httpx.AsyncClient() as client:
                    range_ = int((await client.get(
                        'https://fastly.jsdelivr.net/gh/yzyyz1387/blogimages/nonebot/wordcloud/num.txt')).read())
                    logger.info(f"获取到{range_}张mask图片")
                    for i in range(range_):
                        wordcloud_bg = await client.get(
                            f"https://fastly.jsdelivr.net/gh/yzyyz1387/blogimages/nonebot/wordcloud/bg{i}.png")
                        logger.info(f"正下载{i}张mask图片")
                        with open(plugin_config.wordcloud_bg_path / f"{i}.png", 'wb') as f:
                            f.write(wordcloud_bg.content)
                        f.close()
            except:
                logger.error('下载词云mask图片出现错误')
                return
            wordcloud_bg = random.choice(os.listdir(plugin_config.wordcloud_bg_path))
        background_image = imread(plugin_config.wordcloud_bg_path / wordcloud_bg)
        if gid + '.txt' in dir_list:
            text = path_temp.read_text(encoding='utf-8')
            txt = jieba.lcut(text)
            this_stop_ = plugin_config.stop_words_path / f"{gid}.txt"
            if this_stop_.exists():
                stop_ = set(this_stop_.read_text(encoding='utf-8').split('\n') + (await participle_simple_handle()))
            else:
                stop_ = set(await participle_simple_handle())
            string = ' '.join(txt)
            try:
                wc = WordCloud(font_path=str(ttf_name_.resolve()),
                               width=1920, height=1080, mode='RGBA',
                               background_color='#ffffff',
                               mask=background_image,
                               stopwords=stop_).generate(string)
                img = Path(plugin_config.re_img_path / f"wordcloud_{gid}.png")
                img_colors = ImageColorGenerator(background_image, default_color=(255, 255, 255))
                wc.recolor(color_func=img_colors)
                wc.to_file(img)
                await cloud.send(MessageSegment.image(img))
            except Exception as err:
                await cloud.send(f"出现错误{type(err)}:{err}")
        else:
            await cloud.finish("当前群未被记录，请先在群内发送，【记录本群】")
    except ModuleNotFoundError:
        await cloud.finish('未安装wordcloud库')
