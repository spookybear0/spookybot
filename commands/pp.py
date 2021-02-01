from helpers.np import pp as np
from helpers.config import config
import pyosu

api = pyosu.OsuApi(config["osuapikey"])

async def pp(ctx, args):
    try:
        map = args[1]
    except IndexError:
        return "Invalid arguments."
    
    mode = await api.get_beatmap(beatmap_id=map).mode
    
    return await np(map, 0, mode)