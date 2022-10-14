from typing import List
from helpers.extension import Extension
from helpers.osu import mod_to_num, num_to_mod
from helpers.command import Context
import aiohttp
import re

class NPExtension(Extension):
    def __init__(self) -> None:
        self.name = "np"

    async def on_ready(self, ctx: Context):
        self.expression = re.compile(r"is (?:playing|listening to|editing|watching) \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#.*\/([0-9]+) .*\](?: \+|)(.*|)")

    async def on_message(self, ctx: Context):
        if ctx.message.content.startswith("is "):
            final = ""

            try:
                map_id, mods = self.expression.findall(str(ctx.message.content))[0]
            except IndexError:
                return # no matches, return because it's probably just a message that starts with "is"
            mods_num = mod_to_num(mods)
            map_id = int(map_id)

            map = await ctx.bot.api.get_beatmap(beatmap_id=map_id)

            # ripple api to get pp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map_id}&m={mods_num}&g={map.mode}") as r:
                    req = await r.json()

            pp: List = req["pp"]
            pp.reverse()

            for i in range(4):
                final += f"{i+97}%: {round(pp[i], 2)}pp | "
            
            mods_str = f" +{mods}"
            final += f'{req["song_name"]} | {req["stars"]}* | {req["bpm"]} BPM | AR {req["ar"]}{mods_str}'

            return await ctx.send(final)