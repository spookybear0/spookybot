from helpers.config import load_config, config
try:
    load_config()
except SystemExit:
    exit()

from helpers.parse import parse_args
from helpers.command import parse_commands, init_commands
from helpers.np import pp, process_re
from helpers.classify import Classify
from helpers.bot import init_bot, bot
from helpers.db import add_user, log_command, set_last_beatmap, get_banned, connect_db
import osu_irc, os, re, time, asyncio, nest_asyncio, pyosu
from ratelimiter import RateLimiter

nest_asyncio.apply()
path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(config["osuapikey"])
prefix = "!"
nickname = "spookybear0"
debug = False

class SpookyBot(osu_irc.Client):
    async def onReady(self):
        print("SpookyBot is ready!")
        
    async def onError(self, error):
        print(f"Uncatched error: {error}")

    async def onMessage(self, msg: osu_irc.Message):
        banned = await get_banned(msg.user_name)
        if msg.is_private:
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
                @RateLimiter(max_calls=10, period=5) # user rate limits
                async def send_msg():
                    await add_user(msg.user_name, user.user_id, msg.content) # add user to db
                    await log_command(msg.user_name, user.user_id, msg.content) # log the message
                    
                    if banned:
                        r = "You are banned!"
                    else:
                        r = responce
                    
                    await self.sendPM(msg.user_name, str(r))
                    print(f"Sent {msg.user_name} this \"{r}\"") # debugging
                await send_msg()
            elif msg.content.startswith("is "):
                
                print(f"Got /np from {msg.user_name} which contains this \"{msg.content}\"")
                await log_command(msg.user_name, user.user_id, msg.content)
                
                # get /np
                await add_user(msg.user_name, user.user_id, msg.content)
                
                all = re.findall(r"is playing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)|is listening to \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is editing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is watching \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)",
                str(msg.content))
                
                mods, map_id = process_re(all)
                
                await set_last_beatmap(msg.user_name, map_id)
                
                mode = await api.get_beatmap(beatmap_id=map_id)
                
                result = await pp(map_id, mods, mode.mode)
                
                for r in result.split("\n"):
                    await self.sendPM(msg.user_name, r)
            
                    
async def main():
    global spookybot
    loop = asyncio.get_event_loop()
    
    init_commands()
    
    await connect_db(loop)
    
    token = config["token"]
    
    while True:
        spookybot = SpookyBot(token=token, nickname=nickname)
        print("Starting SpookyBot on discord.")
        await init_bot(spookybot)
        if debug:
            while True: pass
        try:
            if not debug:
                print("Starting SpookyBot.")
                spookybot.run()
        except RuntimeError as e:
            if not debug:
                spookybot.stop()
            print(e)
        except KeyboardInterrupt:
            if not debug:
                spookybot.stop()
            await bot.logout()
        time.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())