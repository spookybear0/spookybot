import asyncio
from typing import Optional, List
from helpers.extension import Extension
from helpers.command import Context
import osu_irc
import re
from extensions.matchmaker import Lobby
import string
import random

class BanchoBot(Extension):
    def __init__(self) -> None:
        self.name = "banchobot"
        self.help = "BanchoBot interaction extension"
        self.bot: Optional[osu_irc.Client] = None
        self.last_mp_id = -1

    async def setup(self, ctx: Context):
        self.bot = ctx.bot
        self.match_create_re = re.compile(r"Created the tournament match https:\/\/osu\.ppy\.sh\/mp\/([0-9]+)")

    async def on_message(self, ctx: Context):
        if ctx.username == "BanchoBot":
            if self.match_create_re.match(ctx.content):
                self.last_mp_id = int(self.match_create_re.findall(ctx.content)[0])
            elif ctx.content.startswith("You cannot create any more tournament matches."):
                if self.last_mp_id != -1:
                    self.last_mp_id = -1
                else:
                    self.last_mp_id = -2

    async def send_command(self, command, *args):
        await self.bot.sendPM("BanchoBot", f"!{command} {' '.join(args)}")

    async def mp_make(self, name):
        prev = self.last_mp_id
        await self.send_command("mp", "make", name)
        while prev == self.last_mp_id:
            await asyncio.sleep(1)
        return await Lobby.create(self.last_mp_id, "".join([random.choice(string.ascii_letters) for x in range(20)]))
    
    async def mp_makeprivate(self, name) -> Lobby:
        prev = self.last_mp_id
        await self.send_command("mp", "makeprivate", name)
        while prev == self.last_mp_id:
            await asyncio.sleep(1)
        return await Lobby.create(self.last_mp_id, "".join([random.choice(string.ascii_letters) for x in range(20)]))