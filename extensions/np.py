from helpers.extension import Extension
from helpers.logger import logger
from helpers.osu import mod_to_num, num_to_mod
from helpers.command import Context
import aiohttp
import re

class NPExtension(Extension):
    def __init__(self) -> None:
        self.name = "np"

    async def on_ready(self, ctx: Context):
        logger.debug("Test extension is ready!")

    async def on_message(self, ctx: Context):
        if ctx.message.content.startswith("is "):
            #is playing [https://osu.ppy.sh/beatmapsets/714359#/1509693 Kondo Koji - Slider [64 DIMENSIONS]] +HardRock
            map_id, mods = re.findall(r"is (?:playing|listening to|editing|watching) \[https:\/\/osu\.ppy\.sh\/beatmapsets\/[0-9]+\#.*\/([0-9]+) .*\](?: \+|)(.*|)",
                            str(ctx.message.content))[0]
            mods_num = mod_to_num(mods)
            map_id = int(map_id)

            map = await ctx.bot.api.get_beatmap(beatmap_id=map_id)

            print(map_id, mods, mods_num, map)

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map}&m={mods}&g={mode}") as r: # ripple api to get pp
                    req = await r.json()

            #r["song_name"] + " |" + final + " " + str(round(r["stars"], 2)) + "* | " + str(r["bpm"]) + " BPM | AR " + str(r["ar"]) + " +" + num_to_mod(mods)
            return await ctx.send(f'{req["song_name"]} | {req["stars"]}* | {req["bpm"]} BPM | AR {req["ar"]} +{num_to_mod(mods)}')