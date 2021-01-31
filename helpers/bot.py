import discord, os, asyncio, pyosu, textwrap
from discord.ext import commands
from helpers.config import config
from helpers.db import ban_user, get_bugs, get_suggestions, get_users, connect_db
from multiprocessing import Process

enabled = True

path = os.path.dirname(os.path.realpath(__file__))
api = pyosu.OsuApi(config["osuapikey"])
bot = commands.Bot(command_prefix="s!")

@bot.command()
@commands.is_owner()
async def ban(ctx: commands.Context, username, reason=""):
    user_id = await api.get_user(username).user_id
    await ban_user(username, user_id, reason)
    
@bot.command()
@commands.is_owner()
async def bugs(ctx: commands.Context):
    result = await get_bugs()
    await ctx.send(f"```{result}```")
    
@bot.command()
@commands.is_owner()
async def suggestions(ctx: commands.Context):
    result = await get_suggestions()
    await ctx.send(f"```{result}```")
    
@bot.command()
@commands.is_owner()
async def users(ctx: commands.Context):
    users = await get_users()
    await ctx.send(f"```{users}```")


@bot.command(name="exec", aliases=["eval"])
@commands.is_owner()
async def exec(ctx, *, body: str):
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)
    env = {
            "bot": bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "discord": discord
        }
    body = body.strip("```py")
    body = body.strip("`")
    body = indent(body, 4)
    to_compile = f"import asyncio\nasync def func():{body}\nresult = asyncio.create_task(func())"
    try:
        loc = {}
        exec(to_compile, env, loc)
    except Exception as e:
        await ctx.message.add_reaction("❌")
        return await ctx.send(f"```\n{e.__class__.__name__}: {e}\n```")
    else:
        await ctx.message.add_reaction("✅")
        result = loc["result"].result()
        return await ctx.send(f"```\n{result}\n```")
    
def start_bot():
    global conn
    from helpers.db import conn
    bot.run(config["discordbottoken"])

async def init_bot():
    if not enabled:
        return
    botprocess = Process(target=start_bot)
    botprocess.start()
    
def stop_bot():
    bot.logout()