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
            final = mapobject.artist + "-" + mapobject.title + "[" + mapobject.version + "] |" + final + " " + str(round(mapobject.difficultyrating, 2)) + "* | " + str(mapobject.bpm) + " BPM | AR " + str(mapobject.diff_approach) + " +" + num_to_mod(mods)
            return final
        except Exception as e:
            return "Mania is not yet supported for pp."
    pp.reverse()
    
    for i in range(4):
        final += f" {i+97}%: {round(pp[i], 2)}pp |"
    final = r["song_name"] + " |" + final + " " + str(round(r["stars"], 2)) + "* | " + str(r["bpm"]) + " BPM | AR " + str(r["ar"]) + " +" + num_to_mod(mods)
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
    
    if "NF" in mods:    total += 1<<0
    if "EZ" in mods:    total += 1<<1
    if "HD" in mods:    total += 1<<3
    if "HR" in mods:    total += 1<<4
    if "SD" in mods:    total += 1<<5
    if "DT" in mods:    total += 1<<6
    if "RX" in mods:    total += 1<<7
    if "HT" in mods:    total += 1<<8
    if "NC" in mods:    total += 1<<9
    if "FL" in mods:    total += 1<<10
    if "SO" in mods:    total += 1<<12
    if "PF" in mods:    total += 1<<14

    return int(total)

def num_to_mod(num):
    mod_list = []

    if num & 1<<0: mod_list.append('NF')
    if num & 1<<1:   mod_list.append('EZ')
    if num & 1<<3:   mod_list.append('HD')
    if num & 1<<4:   mod_list.append('HR')
    if num & 1<<5:   mod_list.append('SD')
    if num & 1<<9:   mod_list.append('NC')
    elif num & 1<<6: mod_list.append('DT')
    if num & 1<<7:   mod_list.append('RX')
    if num & 1<<8:   mod_list.append('HT')
    if num & 1<<10:  mod_list.append('FL')
    if num & 1<<12:  mod_list.append('SO')
    if num & 1<<14:  mod_list.append('PF')
    if num & 1<<15:  mod_list.append('4 KEY')
    if num & 1<<16:  mod_list.append('5 KEY')
    if num & 1<<17:  mod_list.append('6 KEY')
    if num & 1<<18:  mod_list.append('7 KEY')
    if num & 1<<19:  mod_list.append('8 KEY')
    if num & 1<<20:  mod_list.append('FI')
    if num & 1<<24:  mod_list.append('9 KEY')
    if num & 1<<25:  mod_list.append('10 KEY')
    if num & 1<<26:  mod_list.append('1 KEY')
    if num & 1<<27:  mod_list.append('3 KEY')
    if num & 1<<28:  mod_list.append('2 KEY')

    return "".join(mod_list)

def can_be_int(num):
    try:
        int(num)
    except:
        return False
    return True

def process_re(all):
    mods = ""
    map_id = 0 # beatmap id
    
    if all[0][0] != "" and can_be_int(all[0][0]): map_id = int(all[0][0])
    elif all[0][0] != "": mods = all[0][0]
    if all[0][1] != "" and can_be_int(all[0][1]): map_id = int(all[0][1])
    elif all[0][1] != "": mods = all[0][1]
    if all[0][2] != "" and can_be_int(all[0][2]): map_id = int(all[0][2])
    elif all[0][2] != "": mods = all[0][2]
    if all[0][3] != "" and can_be_int(all[0][3]): map_id = int(all[0][3])
    elif all[0][3] != "": mods = all[0][3]
    if all[0][4] != "" and can_be_int(all[0][4]): map_id = int(all[0][4])
    elif all[0][4] != "": mods = all[0][4]
    if all[0][5] != "" and can_be_int(all[0][4]): map_id = int(all[0][5])
    elif all[0][5] != "": mods = all[0][5]
    
    return [mod_to_num(mods[1:]), map_id]

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