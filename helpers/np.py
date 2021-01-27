import http3

client = http3.AsyncClient()

async def pp(map, mods=0):
    final = ""
    r = await client.get(url=f"https://ripple.moe/letsapi/v1/pp?b={map}&m={mods}") # ripple api to get pp
    r = r.json()
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