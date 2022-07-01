from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11.event import MessageEvent

matcher = on_command(
    "计协"
)
new_in = on_notice()

@matcher.handle()
async def learn():
    await matcher.send("Hello World")


