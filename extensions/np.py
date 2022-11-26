from typing import List, Optional
from helpers.extension import Extension
from helpers.osu import mod_to_num, num_to_mod
from helpers.command import Context
import aiohttp
import re

class NPExtension(Extension):
    def __init__(self) -> None:
        self.name = "np"
        self.help = "Gets information about a map."

    async def setup(self, ctx: Context):
        self.expression = re.compile(r"is (?:playing|listening to|editing|watching) \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#.*\/([0-9]+) .*\](?: \+|)(.*|)")

    async def on_message(self, ctx: Context, mods: Optional[int]=None, acc: Optional[float]=None):
        if type(ctx.message) == int or ctx.message.content.startswith("is "):
            final = ""

            try:
                map_id, mods_num = self.expression.findall(str(ctx.message.content))[0]
            except (IndexError, AttributeError):
                try:
                    map_id = int(ctx.message)

                except ValueError:
                    return # no matches, return because it's probably just a message that starts with "is"

            map_id = int(map_id)
            if mods:
                mods_num = mods
            elif acc:
                mods_num = 0
            else:
                mods_num = mod_to_num(mods_num)

            ctx.bot.recent_maps[ctx.username] = map_id

            map = await ctx.bot.api.get_beatmap(beatmap_id=map_id)

            # ripple api to get pp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map_id}&m={mods_num}&g={map.mode}") as r:
                    req = await r.json()
            
            mods_str = ""
            if mods_num:
                mods_str = f" +{num_to_mod(mods_num)}"
                
            final += f'{req["song_name"]}{mods_str} | {round(req["stars"], 2)}* | {req["bpm"]} BPM | AR {req["ar"]}'

            if acc:
                # guess this is broken, TODO: change from ripple api to something else
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map_id}&m={mods_num}&g={map.mode}&a={acc}") as r:
                        req = await r.json()
                final += f" | {acc}%: {round(req['pp'], 2)}pp"
            else:
                pp: List = req["pp"]
                pp.reverse()

                for i in range(4):
                    final += f" | {i+97}%: {round(pp[i], 2)}pp"

            return await ctx.send(final)