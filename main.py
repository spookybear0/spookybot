from helpers.parse import parse_args
from helpers.command import parse_commands
from helpers.np import pp
import osu_irc, os, re
from ratelimiter import RateLimiter

path = os.path.dirname(os.path.realpath(__file__))

prefix = "!"
token = open(path + "/token", "r").read()
nickname = "spookybear0"

def can_be_int(num):
    try:
        int(num)
    except:
        return False
    return True

class SpookyBot(osu_irc.Client):
    async def onReady(self):
        print("SpookyBot is ready!")

    @RateLimiter(max_calls=10, period=5)
    async def onMessage(self, msg):
        print("msg")
        if msg.is_private:
            args = parse_args(msg.content)
            ctx = { # context object to send
                "message": msg,
                "msg": msg,
                "username": msg.user_name,
                "content": msg.content
            }
            responce = await parse_commands(args, ctx)
            if responce: # only send if command detected
                await self.sendPM(msg.user_name, str(responce))
                print("Sent " + msg.user_name + " this \"" + str(responce) + "\"")
            elif msg.content.startswith("is"):
                # get /np
                all = re.findall(r"is playing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)|is listening to \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is editing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is watching \[https://osu\.ppy\.sh/b/([0-9]+) .*\]( .*|)",
                str(msg.content))
                mods = ""
                bid = 0
                if all[0][0] != "" and can_be_int(all[0][0]): bid = int(all[0][0])
                elif all[0][0] != "": mods = all[0][0]
                if all[0][1] != "" and can_be_int(all[0][1]): bid = int(all[0][1])
                elif all[0][1] != "": mods = all[0][1]
                if all[0][2] != "" and can_be_int(all[0][2]): bid = int(all[0][2])
                elif all[0][2] != "": mods = all[0][2]
                if all[0][3] != "" and can_be_int(all[0][3]): bid = int(all[0][3])
                elif all[0][3] != "": mods = all[0][3]
                if all[0][4] != "" and can_be_int(all[0][4]): bid = int(all[0][4])
                elif all[0][4] != "": mods = all[0][4]
                if all[0][5] != "" and can_be_int(all[0][4]): bid = int(all[0][5])
                elif all[0][5] != "": mods = all[0][5]
                mods = mods[1:]
                await self.sendPM(msg.user_name, pp(bid))

if __name__ == "__main__":
    spookybot = SpookyBot(token=token, nickname=nickname)
    try:
        print("Starting SpookyBot")
        spookybot.run()
    except RuntimeError:
        pass
    except KeyboardInterrupt:
        pass