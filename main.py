from helpers.config import load_config, config
try:
    load_config()
except SystemExit:
    exit()

from helpers.parse import parse_args
from helpers.command import parse_commands
from helpers.np import pp, process_re
from helpers.classify import Classify
from helpers.bot import init_bot, bot
from helpers.db import add_user, log_command, connect_db
import osu_irc, os, re, time, asyncio, nest_asyncio, pyosu
from ratelimiter import RateLimiter

nest_asyncio.apply()
path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(config["osuapikey"])
prefix = "!"
nickname = "spookybear0"

class SpookyBot(osu_irc.Client):
    async def onReady(self):
        print("SpookyBot is ready!")
        
    async def onError(self, error):
        print(f"Uncatched error: {error}")

    async def onMessage(self, msg: osu_irc.Message):
        if msg.is_private:
            args = parse_args(msg.content)
            userid = await api.get_user(msg.user_name).user_id
            ctx = Classify({ # context object to send to command
                "message": msg, # message object
                "msg": msg, # alias to message
                "username": msg.user_name,
                "content": msg.content, # raw message contents (not parsed)
                "userid":  userid
            })
            responce = await parse_commands(args, ctx)
            if responce: # only send if command detected
                @RateLimiter(max_calls=10, period=5)
                async def send_msg():
                    await add_user(msg.user_name. msg.user_id, msg.content) # add user to db
                    await log_command(msg.user_name. msg.user_id, msg.content) # log the message
                    
                    await self.sendPM(msg.user_name, str(responce))
                    print(f"Sent {msg.user_name} this \"{responce}\"") # debugging
                await send_msg()
            elif msg.content.startswith("is "):
                # get /np
                await add_user(msg.user_name. msg.user_id, msg.content)
                
                all = re.findall(r"is playing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)|is listening to \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is editing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is watching \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)",
                str(msg.content))
                
                result = await pp(*process_re(all))
                
                for r in result.split("\n"):
                    await self.sendPM(msg.user_name, r)
                    
async def main():
    loop = asyncio.get_event_loop()
    
    loop.create_task(init_bot())
    
    token = config["token"]

    await connect_db(loop)
    
    while True:
        spookybot = SpookyBot(loop, token=token, nickname=nickname)
        try:
            print("Starting SpookyBot")
            spookybot.run()
        except RuntimeError as e:
            print(e)
        except KeyboardInterrupt:
            pass
        time.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())