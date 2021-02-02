import aiohttp, pyosu, time, os
from helpers.config import config
from maniera.calculator import Maniera

api = pyosu.OsuApi(config["osuapikey"])

async def pp(map, mods=0, mode=0):
    final = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map}&m={mods}&g={mode}") as r: # ripple api to get pp
            r = await r.json()
    
    try:
        pp = r["pp"]
    except KeyError: # gamemode not supported / mania
        try:
            scores = [1000000, 900000, 750000]
            pp = []
            
            mapobject = await api.get_beatmap(beatmap_id=map)
            
            for s in scores:
                pp.append(await mania_pp(map, mods, s))

            i = 0
            for s in scores:
                final += f" {s}: {round(pp[i], 2)}pp |"
                i += 1
            final = mapobject.artist + "-" + mapobject.title + "[" + mapobject.version + "] |" + final + " " + str(round(mapobject.difficultyrating, 2)) + "* | " + str(mapobject.bpm) + " BPM | AR " + str(mapobject.diff_approach)
            return final
        except Exception as e:
            return "Mania is not yet supported for pp."
    pp.reverse()
    
    for i in range(4):
        final += f" {i+97}%: {round(pp[i], 2)}pp |"
    final = r["song_name"] + " |" + final + " " + str(round(r["stars"], 2)) + "* | " + str(r["bpm"]) + " BPM | AR " + str(r["ar"])
    return final

def mod_to_num(mods):
    total = 0
    
    if mods == "":
        return 0

    if "NoFail" in mods:    total += 1<<0
    if "Easy" in mods:    total += 1<<1
    if "Hidden" in mods:    total += 1<<3
    if "HardRock" in mods:    total += 1<<4
    if "SuddenDeath" in mods:    total += 1<<5
    if "DoubleTime" in mods:    total += 1<<6
    if "Relax" in mods:    total += 1<<7
    if "HalfTime" in mods:    total += 1<<8
    if "Nightcore" in mods:    total += 1<<9
    if "Flashlight" in mods:    total += 1<<10
    if "SpunOut" in mods:    total += 1<<12
    if "Perfect" in mods:    total += 1<<14

    return int(total)

def can_be_int(num):
    try:
        int(num)
    except:
        return False
    return True

def process_re(all):
    mods = ""
    bid = 0 # beatmap id
    
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
    
    return [mod_to_num(mods[1:]), bid]

async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return await response.release()

async def mania_pp(map_id: int, mods: int, score: int):
    url = f"https://osu.ppy.sh/osu/{map_id}"
    filepath = f"data/osu/temp/"
    
    try:
        os.makedirs(filepath)
    except Exception:
        pass
    
    await download_file(url, filepath + "{map_id}.osu")
    
    calc = Maniera(filepath + "{map_id}.osu", mods, score)
    calc.calculate()
    
    return round(calc.pp, 2)