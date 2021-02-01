import aiohttp

async def pp(map, mods=0, mode=0):
    final = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://ripple.moe/letsapi/v1/pp?b={map}&m={mods}&g={mode}") as r: # ripple api to get pp
            r = await r.json()
    
    try:
        pp = r["pp"]
    except KeyError: # gamemode not supported
        final += "Only osu!standard is supported for pp.\n"
        pp = [0.00]
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