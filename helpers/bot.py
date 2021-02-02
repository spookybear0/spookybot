from spook.spookybot.helpers.db import remove_user
import discord, os, asyncio, pyosu, textwrap, osu_irc, re
from discord.ext import commands
from helpers.config import config
from helpers.parse import parse_args
from helpers.classify import Classify
from helpers.command import parse_commands, init_commands
from helpers.db import ban_user, get_bugs, get_suggestions, get_users, unban_user, connect_db, log_command, set_last_beatmap, add_user
from helpers.np import pp, process_re
from contextlib import redirect_stdout
from io import StringIO
import multiprocessing as mp

enabled = True

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
async def unban(ctx: commands.Context, username):
    await unban_user(username)
    await ctx.send("Unbanned user!")
    
@bot.command()
@commands.is_owner()
async def unban_id(ctx: commands.Context, user_id):
    await unban_user(None, user_id)
    await ctx.send("Unbanned user!")
    
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
async def _exec(ctx, *, body: str):
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
    body = indent(body.replace("```py", "").strip("`"), 4)
    result = None
    to_compile = f"import asyncio\nasync def func():\n{body}\nresult = asyncio.run(func())"
    
    loc = {}
    stdout = StringIO() 
    try:
        with redirect_stdout(stdout):
            exec(to_compile, env, loc)
    except Exception as e:
        await ctx.message.add_reaction("❌")
        return await ctx.send(f"```\n{e.__class__.__name__}: {e}\n```")
    else:
        await ctx.message.add_reaction("✅")
        result = loc["result"]
        stdout = stdout.getvalue()[:-1]
        
        if stdout:
            await ctx.send(f"stdout \n```\n{stdout}\n```")
        if result:
            await ctx.send(f"return value \n```\n{result}\n```")
    
async def onMessage(msg: osu_irc.Message): # fake
    init_commands()
    args = parse_args(msg.content)
    user = await api.get_user(msg.user_name)
    ctx = Classify({ # context object to send to command
        "message": msg, # message object
        "msg": msg, # alias to message
        "username": msg.user_name,
        "content": msg.content, # raw message contents (not parsed)
        "userid":  user.user_id
    })
    responce = await parse_commands(args, ctx)
    if responce: # only send if command detected
        async def send_msg():
            await add_user(msg.user_name, user.user_id, msg.content) # add user to db
            await log_command(msg.user_name, user.user_id, msg.content) # log the message

            print(f"TEST Sent {msg.user_name} this \"{responce}\"")
            return str(responce)
        r = await send_msg()
        return r
    elif msg.content.startswith("is "):
        # get /np
        await add_user(msg.user_name, user.user_id, msg.content)
                
        all = re.findall(r"is playing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)|is listening to \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is editing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is watching \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)",
        str(msg.content))
                
        mods, bid = process_re(all) # bid = beatmap id
                
        await set_last_beatmap(msg.user_name, bid)
                
        mode = await api.get_beatmap(beatmap_id=map).mode
                
        result = await pp(bid, mods, mode)
                
        for r in result.split("\n"):
            return r
    
@bot.command()
@commands.is_owner()
async def msg(ctx: commands.Context, *, msg: str):
    try: message = osu_irc.Message(msg)
    except AttributeError: message = osu_irc.Message(" ".join(msg))
    message._user_name = "spookybear0"
    message._content = " ".join(msg)

    r = await onMessage(message)
    
    await ctx.send(f"```{r}```") # fake message
    
@bot.command(name="add_user")
@commands.is_owner()
async def _add_user(ctx: commands.Context, username, userid, content=""):
    await add_user(username, userid, content)
    await ctx.send("User added!")
    
@bot.command(name="remove_user")
@commands.is_owner()
async def _remove_user(ctx: commands.Context, username):
    await remove_user(username)
    await ctx.send("User removed!")

@bot.command(name="remove_user_id")
@commands.is_owner()
async def _remove_user_id(ctx: commands.Context, userid):
    await remove_user(user_id=userid)
    await ctx.send("User removed!")

def start_bot():
    global conn
    asyncio.run(connect_db(asyncio.get_event_loop()))
    from helpers.db import conn
    bot.run(config["discordbottoken"])

async def init_bot(spookybot):
    if not enabled:
        return
    mp.set_start_method("spawn")
    botprocess = mp.Process(target=start_bot)
    botprocess.start()
    
def stop_bot():
    bot.logout()