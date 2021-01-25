import pyosu, os

path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())

modes = {
    "osu": 0,
    "osu!": 0,
    "osu!std": 0,
    "standard": 0,
    "osu!standard": 0,
    "taiko": 1,
    "osu!taiko": 1,
    "ctb": 2,
    "catch": 2,
    "osu!ctb": 2,
    "osu!catch": 2,
    "mania": 3,
    "osu!mania": 3,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3
}

def num_to_mod(number):
    number = int(number)
    mod_list = []

    if number & 1<<0:   mod_list.append("NF")
    if number & 1<<1:   mod_list.append("EZ")
    if number & 1<<3:   mod_list.append("HD")
    if number & 1<<4:   mod_list.append("HR")
    if number & 1<<5:   mod_list.append("SD")
    if number & 1<<9:   mod_list.append("NC")
    elif number & 1<<6: mod_list.append("DT")
    if number & 1<<7:   mod_list.append("RX")
    if number & 1<<8:   mod_list.append("HT")
    if number & 1<<10:  mod_list.append("FL")
    if number & 1<<12:  mod_list.append("SO")
    if number & 1<<14:  mod_list.append("PF")
    if number & 1<<15:  mod_list.append("4 KEY")
    if number & 1<<16:  mod_list.append("5 KEY")
    if number & 1<<17:  mod_list.append("6 KEY")
    if number & 1<<18:  mod_list.append("7 KEY")
    if number & 1<<19:  mod_list.append("8 KEY")
    if number & 1<<20:  mod_list.append("FI")
    if number & 1<<24:  mod_list.append("9 KEY")
    if number & 1<<25:  mod_list.append("10 KEY")
    if number & 1<<26:  mod_list.append("1 KEY")
    if number & 1<<27:  mod_list.append("3 KEY")
    if number & 1<<28:  mod_list.append("2 KEY")

    return mod_list

async def top(ctx, args):
    print(os.getenv("OSUAPIKEY"))
    api = pyosu.OsuApi(os.getenv("OSUAPIKEY"))
    try:
        amount = int(args[1])
    except IndexError:
        amount = 1
    else:
        if amount > 5:
            amount = 5
    try:
        username = args[2]
    except IndexError:
        username = ctx.username
    try:
        mode = modes.get(args[3]) # switch statement (None if not True)
    except IndexError:
        mode = 0
    else:
        if not mode:
            mode = 0
    if amount == 1:
        best = await api.get_user_best(username, mode, "string")
        map = await api.get_beatmap(beatmap_id=best.beatmap_id)
        perfect = ""
        if not best.perfect:
            perfect = "| PERFECT"
        acc = (best.count300 + (best.count100/3) + (best.count50/6))/map.max_combo
        return f"{map.artist} - {map.title} [{map.version}] {round(acc, 2)}% {num_to_mod(best.enabled_mods)} {round(map.difficultyrating, 2)}* | {best.rank} | {best.pp}pp | {int(best.score)} | {best.maxcombo} | {best.count300} x 300, {best.count100} x 100, {best.count50} x 50, {best.countmiss} miss {perfect}"
    else:
        return "Getting multiple top plays isn't supported yet, check back later."
        bests = await api.get_user_bests(username, mode, "string", amount)