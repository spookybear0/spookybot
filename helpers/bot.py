import discord, os, asyncio, threading, pyosu
from discord.ext import commands
from helpers.config import config
from helpers.db import ban_user, get_bugs, get_suggestions

enabled = False

path = os.path.dirname(os.path.realpath(__file__))
api = pyosu.OsuApi(config["osuapikey"])
bot = commands.Bot(command_prefix="!")

@bot.command()
@commands.is_owner()
async def ban(ctx: commands.Context, username, reason=""):
    user_id = await api.get_user(username).user_id
    await ban_user(username, user_id, reason)
    
@bot.command()
@commands.is_owner()
async def bugs(ctx: commands.Context, username, reason=""):
    bugs = await get_bugs()
    await ctx.send(f"```{bugs}```")
    
@bot.command()
@commands.is_owner()
async def suggestions(ctx: commands.Context, username, reason=""):
    suggestions = await get_suggestions()
    await ctx.send(f"```{suggestions}```")

def bot_thread_func(loop: asyncio.BaseEventLoop):
    asyncio.set_event_loop(loop)
    asyncio.run(bot.start(config["discordbottoken"]))

async def init_bot():
    if not enabled:
        return
    
    bot_thread = threading.Thread(target=bot_thread_func, args=(asyncio.get_event_loop(),))
    bot_thread.start()
    
def stop_bot():
    bot.logout()