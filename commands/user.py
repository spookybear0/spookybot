import pyosu, os

path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())

async def user(ctx, args):
    global api
    if not os.getenv("OSUAPIKEY"):
        api = pyosu.OsuApi(os.getenv("OSUAPIKEY"))
    try:
        username = args[1]
    except IndexError:
        username = ctx.username
    try:
        mode = args[2]
    except IndexError:
        mode = 0
    u = await api.get_user(username, mode)
    try:
        return f"{username} has {u.pp_raw}pp and is rank #{u.pp_rank} globally and #{u.pp_country_rank} rank in {u.country}."
    except AttributeError:
        return "User not found!"
    
aliases = ["osu"]