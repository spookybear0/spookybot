import os, pyosu, pyoppai, aiohttp
from helpers.config import config

path = os.path.dirname(os.path.realpath(__file__))

api = pyosu.OsuApi(config["osuapikey"])

def acc_calc(n300, n100, n50, misses):
    """calculates accuracy (0.0-1.0)"""
    h = n300 + n100 + n50 + misses

    if h <= 0:
        return 0.0

    return (n50 * 50.0 + n100 * 100.0 + n300 * 300.0) / (h * 300.0) * 100

def num_to_mod(number):
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

# from owo bot

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

async def py_oppai(map_id:str, accs=[100], mods=0, misses=0, combo=None, fc=None):
    url = 'https://osu.ppy.sh/osu/{}'.format(map_id)

    # try:
    ctx = pyoppai.new_ctx()
    b = pyoppai.new_beatmap(ctx)

    BUFSIZE = 2000000
    buf = pyoppai.new_buffer(BUFSIZE)

    file_path = 'data/osu/temp/{}.osu'.format(map_id) # some unique filepath
    await download_file(url, file_path) # this is the file name that it downloaded
    pyoppai.parse(file_path, b, buf, BUFSIZE, True, 'data/osu/cache/')
    dctx = pyoppai.new_d_calc_ctx(ctx)
    pyoppai.apply_mods(b, mods)

    stars, aim, speed, _, _, _, _ = pyoppai.d_calc(dctx, b)
    cs, od, ar, hp = pyoppai.stats(b)

    if not combo:
        combo = pyoppai.max_combo(b)

    total_pp_list = []
    aim_pp_list = []
    speed_pp_list = []
    acc_pp_list = []

    for acc in accs:
        accurracy, pp, aim_pp, speed_pp, acc_pp = pyoppai.pp_calc_acc(ctx, aim, speed, b, acc, mods, combo, misses)
        total_pp_list.append(pp)
        aim_pp_list.append(aim_pp)
        speed_pp_list.append(speed_pp)
        acc_pp_list.append(acc_pp)

    if fc:
        _, fc_pp, _, _, _ = pyoppai.pp_calc_acc(ctx, aim, speed, b, fc, mods, pyoppai.max_combo(b), 0)
        total_pp_list.append(fc_pp)

    pyoppai_json = {
        'version': pyoppai.version(b),
        'title': pyoppai.title(b),
        'artist': pyoppai.artist(b),
        'creator': pyoppai.creator(b),
        'combo': combo,
        'misses': misses,
        'max_combo': pyoppai.max_combo(b),
        'mode': pyoppai.mode(b),
        'num_objects': pyoppai.num_objects(b),
        'num_circles': pyoppai.num_circles(b),
        'num_sliders': pyoppai.num_sliders(b),
        'num_spinners': pyoppai.num_spinners(b),
        'stars': stars,
        'aim_stars': aim,
        'speed_stars': speed,
        'pp': total_pp_list, # list
        'aim_pp': aim_pp_list,
        'speed_pp': speed_pp_list,
        'acc_pp': acc_pp_list,
        'acc': accs, # list
        'cs': cs,
        'od': od,
        'ar': ar,
        'hp': hp
        }

    os.remove(file_path)
    return pyoppai_json
    #except:
        #return None

# end from owo bot

async def recent(ctx, args):
    if os.getenv("OSUAPIKEY"):
        api = pyosu.OsuApi(os.getenv("OSUAPIKEY"))
    else:
        api = pyosu.OsuApi(open(path + "/../osuapikey", "r").read())
        
    try:
        username = args[1]
    except IndexError:
        username = ctx.username
        
    try:
        mode = args[2]
    except IndexError:
        mode = 0
        
    recent = await api.get_user_recent(username, mode, "string")
    map = await api.get_beatmap(beatmap_id=recent.beatmap_id)
    acc = acc_calc(recent.count300, recent.count100, recent.count50, recent.countmiss)
    perfect = ""
    if not recent.perfect:
        perfect = "| PERFECT"
    # pp calc
    if recent.rank == "F":
        try:
            pp = await py_oppai(recent.map_id, acc, mods=recent.mods, misses=recent.misses, combo=recent.maxcombo, fc=recent.perfect)["pp"]
        except:
            pp = "pp unavailable"
    else: 
        score = await api.get_score(map.beatmap_id, user=username)
        pp = round(score.pp, 2)
    mods = " ".join(num_to_mod(recent.enabled_mods))
    if mods:
        mods = " +" + mods
    return f"{map.artist} - {map.title} [{map.version}]{mods} {round(acc, 2)}% *{round(map.difficultyrating, 2)} | {recent.rank} | {pp}pp | {int(recent.score)} | {recent.maxcombo}x | {recent.count300} x 300, {recent.count100} x 100, {recent.count50} x 50, {recent.countmiss} miss {perfect}"

aliases = ["rs", "replay", "last"]