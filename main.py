from helpers.parse import parse_args
from helpers.command import parse_commands
from helpers.np import pp
import osu_irc, os, requests, re

path = os.path.dirname(os.path.realpath(__file__))

prefix = "!"
token = open(path + "/token", "r").read()
nickname = "spookybear0"

class SpookyBot(osu_irc.Client):
    async def onReady(self):
        print("SpookyBot is ready!")

    async def onMessage(self, msg):
        print(msg.content)
        if msg.is_private:
            print(msg.user_name + " " +  msg.content)
            args = parse_args(msg.content)
            responce = parse_commands(args)
            if responce: # only send if command detected
                await self.sendPM(msg.user_name, str(responce))
                print("Sent "+ msg.user_name + " this \"" + str(responce) + "\"")
            elif msg.content.startswith("is"):
                all = re.findall(r"is playing \[https://osu\.ppy\.sh/b/([0-9]+) .*\]|is listening to \[https://osu\.ppy\.sh/b/([0-9]+) .*\]", str(msg.content))
                print(all)
                await self.sendPM(msg.user_name, pp(all[0][1]))

if __name__ == "__main__":
    spookybot = SpookyBot(token=token, nickname=nickname)
    try:
        print("Starting SpookyBot")
        spookybot.run()
    except RuntimeError:
        pass
    except KeyboardInterrupt:
        pass