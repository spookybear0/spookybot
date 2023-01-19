from typing import List, Optional
from helpers.extension import Extension
from helpers.osu import mod_to_num, num_to_mod, py_oppai
from helpers.command import Context
import aiohttp
import re

class NPExtension(Extension):
    def __init__(self) -> None:
        self.name = "np"
        self.help = "Gets information about a map."

    async def setup(self, ctx: Context) -> None:
        self.expression = re.compile(r"is (?:playing|listening to|editing|watching) \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#.*\/([0-9]+) .*\](?: \+|)(.*|)")

    async def on_message(self, ctx: Context, mods: Optional[int]=None, acc: Optional[float]=None) -> Optional[str]:

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
            if mods is not None:
                mods_num = mods
            elif acc:
                mods_num = 0
            else:
                mods_num = mod_to_num(mods_num)

            ctx.bot.recent_maps[ctx.username] = map_id

            map = await ctx.bot.api.get_beatmap(beatmap_id=map_id)

            req = await py_oppai(map_id, mods=mods_num, accs=[95, 98, 99, 100])
            
            mods_str = ""
            if mods_num:
                mods_str = f" +{num_to_mod(mods_num)}"
                
            final += f'[https://osu.ppy.sh/beatmapsets/{map.beatmapset_id}#osu/{map_id} {map.artist} - {map.title} [{map.version}]]{mods_str} | {round(req["stars"], 2)}* | {int(map.bpm)} BPM | AR {round(req["ar"], 2)}'

            if acc:
                req = await py_oppai(map_id, mods=mods_num, accs=[acc])
                final += f" | {acc}%: {round(req['pp'][0], 2)}pp"
            else:
                pp: List = req["pp"]

                for i in range(4):
                    final += f" | {i+97}%: {round(pp[i], 2)}pp"
            
            if type(ctx.message) == int:
                return final
            await ctx.send(final)