import requests, os, pyosu, asyncio

path = os.path.dirname(os.path.realpath(__file__))

token = open(path + "/../token", "r").read()

api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())

def num_to_mod(number):
    """This is the way pyttanko does it. 
    Just as an actual bitwise instead of list. 
    Deal with it."""
    number = int(number)
    mod_list = []

    if number & 1<<0:   mod_list.append('NF')
    if number & 1<<1:   mod_list.append('EZ')
    if number & 1<<3:   mod_list.append('HD')
    if number & 1<<4:   mod_list.append('HR')
    if number & 1<<5:   mod_list.append('SD')
    if number & 1<<9:   mod_list.append('NC')
    elif number & 1<<6: mod_list.append('DT')
    if number & 1<<7:   mod_list.append('RX')
    if number & 1<<8:   mod_list.append('HT')
    if number & 1<<10:  mod_list.append('FL')
    if number & 1<<12:  mod_list.append('SO')
    if number & 1<<14:  mod_list.append('PF')
    if number & 1<<15:  mod_list.append('4 KEY')
    if number & 1<<16:  mod_list.append('5 KEY')
    if number & 1<<17:  mod_list.append('6 KEY')
    if number & 1<<18:  mod_list.append('7 KEY')
    if number & 1<<19:  mod_list.append('8 KEY')
    if number & 1<<20:  mod_list.append('FI')
    if number & 1<<24:  mod_list.append('9 KEY')
    if number & 1<<25:  mod_list.append('10 KEY')
    if number & 1<<26:  mod_list.append('1 KEY')
    if number & 1<<27:  mod_list.append('3 KEY')
    if number & 1<<28:  mod_list.append('2 KEY')

    return mod_list

async def recent(ctx, args):
    try:
        username = args[1]
    except IndexError:
        username = ctx["username"]
    try:
        mode = args[2]
    except IndexError:
        mode = 0
    recent = await api.get_user_recent(username, mode, "string")
    map = await api.get_beatmap(beatmap_id=recent.beatmap_id)
    perfect = ""
    if not recent.perfect:
        perfect = "| PERFECT"
    # pp calc
    pp = await api.get_score(map.beatmap_id, user=username)
    pp = round(pp.pp, 1)
    return f"{map.artist} - {map.title} [{map.version}] {num_to_mod(recent.enabled_mods)} *{round(map.difficultyrating, 2)} | {recent.rank} | {pp}pp | {int(recent.score)} | {recent.maxcombo} | {recent.count300} x 300, {recent.count100} x 100, {recent.count50} x 50, {recent.countmiss} miss {perfect}"