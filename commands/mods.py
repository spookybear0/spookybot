from helpers.np import mod_to_num, pp
from helpers.db import get_last_beatmap
from helpers.config import config
import pyosu

api = pyosu.OsuApi(config["osuapikey"])

async def mods(ctx, args):
    try:
        modlist = args[1]
    except:
        modlist = 0
    
    map = await get_last_beatmap(ctx.username)
    
    map = map[0][0]
    
    if not map:
        return "No recent map!"
    
    mode = await api.get_beatmap(beatmap_id=map)
    
    return await pp(map, mod_to_num(modlist), mode.mode)

aliases = ["with"]