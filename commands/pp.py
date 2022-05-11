from helpers.np import pp as np
from helpers.config import config
from helpers.db import set_last_beatmap
import pyosu
import os

async def pp(ctx, args):
    if os.getenv("OSUAPIKEY"):
        api = pyosu.OsuApi(os.getenv("OSUAPIKEY"))
    else:
        api = pyosu.OsuApi(config["osuapikey"])
    
    try:
        map = args[1]
    except IndexError:
        return "Invalid arguments."
    
    mode = await api.get_beatmap(beatmap_id=map)
    
    if ctx:
        await set_last_beatmap(ctx.username, map)
    
    return await np(map, 0, mode.mode)