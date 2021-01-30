import discord, os, asyncio, threading, time
from discord.ext import commands

enabled = False

path = os.path.dirname(os.path.realpath(__file__))
bot = commands.Bot(command_prefix="!")

def bot_thread_func(loop: asyncio.BaseEventLoop):
    asyncio.set_event_loop(loop)
    asyncio.run(bot.start(open(path + "/../discordtoken", "r").read()))

async def init_bot():
    if not enabled:
        return
    
    bot_thread = threading.Thread(target=bot_thread_func, args=(asyncio.get_event_loop(),))
    bot_thread.start()
    
def stop_bot():
    bot.logout()