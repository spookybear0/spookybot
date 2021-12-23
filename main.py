try:
    from asyncio.exceptions import CancelledError
except ModuleNotFoundError:
    from asyncio import CancelledError
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
from helpers.multi import Match
import osu_irc, os, re, time, asyncio, nest_asyncio, pyosu, pymysql
from threading import Thread
from ratelimiter import RateLimiter

nest_asyncio.apply()
path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(config["osuapikey"])
prefix = "!"
nickname = "spookybear0"

games_open = []
recent_mp_id = 0

class SpookyBot(osu_irc.Client):
    async def onReady(self):
        from helpers.db import conn # db loaded
        self.conn = conn
        #await self.ping_mysql()
        print("SpookyBot is ready!")
        
        # create matches
        await self.create_match("5-6.99* | SpookyBot Map Queue | Testing (!info)")
        await asyncio.sleep(3)
        await self.create_match("4-5.99* | SpookyBot Map Queue | Testing (!info)")
        await asyncio.sleep(3)
        await self.create_match("3-4.99* | SpookyBot Map Queue | Testing (!info)")
        
    async def create_match(self, name: str):
        global recent_mp_id
        prev = recent_mp_id
        # send pm to banchobot
        await self.sendPM("BanchoBot", f"!mp make {name}")
        while prev == recent_mp_id:
            await asyncio.sleep(1)
        match = await Match.create(self, recent_mp_id, name)
        games_open.append(match)
        return match
        
    async def onError(self, error):
        print(f"Uncatched error: {error}")
        
    async def ping_mysql(self):
        print("Pinging mysql!")
        await self.conn.ping()
        await asyncio.sleep(600)
        return (await self.ping_mysql())

    async def onMessage(self, msg: osu_irc.Message):
        #banned = await get_banned(msg.user_name)
        if msg.room_name.startswith("mp_"):
            global games_open
            mp_id = re.findall(r"mp_([0-9]+)", msg.room_name)[0]
            for game in games_open:
                if game.mp_id == int(mp_id):
                    user = await api.get_user(msg.user_name)
                    ctx = Classify({ # context object to send to command
                        "message": msg, # message object
                        "msg": msg, # alias to message
                        "username": msg.user_name,
                        "content": msg.content, # raw message contents (not parsed)
                        "userid":  user.user_id,
                        "bot": self,
                        "match": game
                    })
                    if msg.user_name == "BanchoBot":
                        await game.onMultiEvent(ctx)
                    else:
                        await game.onMessage(ctx)
            return
        
        if msg.is_private:
            args = parse_args(msg.content)
            user = await api.get_user(msg.user_name)
            
            if msg.user_name == "BanchoBot":
                if msg.content.startswith("You cannot create any more"):
                    return
                global recent_mp_id
                mp_id = int(re.findall(r"Created the tournament match https:\/\/osu\.ppy\.sh\/mp\/([0-9]+)", msg.content)[0])
                recent_mp_id = mp_id
            
            ctx = Classify({ # context object to send to command
                "message": msg, # message object
                "msg": msg, # alias to message
                "username": msg.user_name,
                "content": msg.content, # raw message contents (not parsed)
                "userid":  user.user_id,
                "bot": self,
                "match": None
            })
            responce = await parse_commands(args, ctx)
            if responce: # only send if command detected
                @RateLimiter(max_calls=10, period=5) # user rate limits
                async def send_msg():
                    await add_user(msg.user_name, user.user_id, msg.content) # add user to db
                    await log_command(msg.user_name, user.user_id, msg.content) # log the message
                    
                    #if banned:
                    #    return
                    #else:
                    r = responce
                    
                    await self.sendPM(msg.user_name, str(r))
                    print(f"Sent {msg.user_name} this \"{r}\"") # debugging
                await send_msg()
        if msg.content.startswith("is "):
            user = await api.get_user(msg.user_name)

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
    
    spookybot = SpookyBot(token=token, nickname=nickname)
    print("Starting SpookyBot on discord.")
    await init_bot(spookybot)

    try:
        print("Starting SpookyBot.")
        spookybot.run()
    except RuntimeError as e:
        print(e)
    except KeyboardInterrupt:
        await bot.logout()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (RuntimeError, KeyboardInterrupt, CancelledError, ConnectionResetError):
        print("Closing Games")
        for i, game in enumerate(games_open):
            if i != 0:
                time.sleep(5)
            asyncio.run(spookybot.joinChannel(f"mp_{game.mp_id}"))
            asyncio.run(spookybot.sendMessage(f"mp_{game.mp_id}", "!mp close"))
        spookybot.stop()