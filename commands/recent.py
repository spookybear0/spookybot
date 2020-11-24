import requests, os, pyosu, asyncio

path = os.path.dirname(os.path.realpath(__file__))

token = open(path + "/../token", "r").read()

api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())

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
    return f"{map.artist} - {map.title} [{map.version}] *{round(map.difficultyrating, 2)} | {recent.rank} | {pp}pp | {int(recent.score)} | {recent.maxcombo} | {recent.count300} x 300, {recent.count100} x 100, {recent.count50} x 50, {recent.countmiss} miss {perfect}"