import pyosu, os

path = os.path.dirname(os.path.realpath(__file__))
token = open(path + "/../token", "r").read()
api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())

async def getuser(ctx, args):
    try:
        username = args[1]
    except IndexError:
        username = ctx["username"]
    try:
        mode = args[2]
    except IndexError:
        mode = 0
    user = await api.get_user(username, mode)
    return f"{username} has {user.pp_raw}pp and is at #{user.pp_rank} rank globally and #{user.pp_country_rank} rank in {user.country}."