import aiohttp
import pyoppai
import time
import os


class DictDecay(dict):
    """
    Used if values are not needed after a certain amount of time
    """
    def __init__(self, decay_after: int=900, *args, **kwargs):
        """
        decay_after is in seconds
        """
        self.decay_after = decay_after
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, (value, time.time()))

    def __getitem__(self, key):
        if (time.time() - super().__getitem__(key)[1]) > self.decay_after:
            del self[key]
            return None
        return super().__getitem__(key)[0]

    def __repr__(self):
        dict_ = {}
        for key, value in self.items():
            dict_[key] = value[0]
        return f"{self.__class__.__name__}({self.decay_after}, {dict_})"

async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, "wb") as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return await response.release()

async def py_oppai(map_id:str, accs=[100], mods=0, misses=0, combo=None, fc=None):
    url = "https://osu.ppy.sh/osu/{}".format(map_id)

    ctx = pyoppai.new_ctx()
    b = pyoppai.new_beatmap(ctx)

    BUFSIZE = 2000000
    buf = pyoppai.new_buffer(BUFSIZE)

    file_path = "data/osu/temp/{}.osu".format(map_id) # some unique filepath
    await download_file(url, file_path) # this is the file name that it downloaded
    pyoppai.parse(file_path, b, buf, BUFSIZE, True, "data/osu/cache/")
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
        "version": pyoppai.version(b),
        "title": pyoppai.title(b),
        "artist": pyoppai.artist(b),
        "creator": pyoppai.creator(b),
        "combo": combo,
        "misses": misses,
        "max_combo": pyoppai.max_combo(b),
        "mode": pyoppai.mode(b),
        "num_objects": pyoppai.num_objects(b),
        "num_circles": pyoppai.num_circles(b),
        "num_sliders": pyoppai.num_sliders(b),
        "num_spinners": pyoppai.num_spinners(b),
        "stars": stars,
        "aim_stars": aim,
        "speed_stars": speed,
        "pp": total_pp_list, # list
        "aim_pp": aim_pp_list,
        "speed_pp": speed_pp_list,
        "acc_pp": acc_pp_list,
        "acc": accs, # list
        "cs": cs,
        "od": od,
        "ar": ar,
        "hp": hp
        }

    os.remove(file_path)
    return pyoppai_json

def mod_to_num(mods) -> int:
    total = 0
    
    if mods == "":
        return 0

    if "NoFail" in mods: total += 1<<0
    if "Easy" in mods: total += 1<<1
    if "Hidden" in mods: total += 1<<3
    if "HardRock" in mods: total += 1<<4
    if "SuddenDeath" in mods: total += 1<<5
    if "DoubleTime" in mods: total += 1<<6
    if "Relax" in mods: total += 1<<7
    if "HalfTime" in mods: total += 1<<8
    if "Nightcore" in mods: total += 1<<9
    if "Flashlight" in mods: total += 1<<10
    if "SpunOut" in mods: total += 1<<12
    if "Perfect" in mods: total += 1<<14
    
    mods = mods.upper()
    
    if "NF" in mods: total += 1<<0
    if "EZ" in mods: total += 1<<1
    if "HD" in mods: total += 1<<3
    if "HR" in mods: total += 1<<4
    if "SD" in mods: total += 1<<5
    if "DT" in mods: total += 1<<6
    if "RX" in mods: total += 1<<7
    if "HT" in mods: total += 1<<8
    if "NC" in mods: total += 1<<9
    if "FL" in mods: total += 1<<10
    if "SO" in mods: total += 1<<12
    if "PF" in mods: total += 1<<14

    return int(total)

def num_to_mod(num) -> str:
    mod_list = []

    if num & 1<<0:   mod_list.append("NF")
    if num & 1<<1:   mod_list.append("EZ")
    if num & 1<<3:   mod_list.append("HD")
    if num & 1<<4:   mod_list.append("HR")
    if num & 1<<5:   mod_list.append("SD")
    if num & 1<<9:   mod_list.append("NC")
    elif num & 1<<6: mod_list.append("DT")
    if num & 1<<7:   mod_list.append("RX")
    if num & 1<<8:   mod_list.append("HT")
    if num & 1<<10:  mod_list.append("FL")
    if num & 1<<12:  mod_list.append("SO")
    if num & 1<<14:  mod_list.append("PF")
    if num & 1<<15:  mod_list.append("4 KEY")
    if num & 1<<16:  mod_list.append("5 KEY")
    if num & 1<<17:  mod_list.append("6 KEY")
    if num & 1<<18:  mod_list.append("7 KEY")
    if num & 1<<19:  mod_list.append("8 KEY")
    if num & 1<<20:  mod_list.append("FI")
    if num & 1<<24:  mod_list.append("9 KEY")
    if num & 1<<25:  mod_list.append("10 KEY")
    if num & 1<<26:  mod_list.append("1 KEY")
    if num & 1<<27:  mod_list.append("3 KEY")
    if num & 1<<28:  mod_list.append("2 KEY")

    return "".join(mod_list)

def acc_calc(n300, n100, n50, misses) -> float:
    """calculates accuracy (0.0-1.0)"""
    h = n300 + n100 + n50 + misses

    if h <= 0:
        return 0.0

    return (n50 * 50.0 + n100 * 100.0 + n300 * 300.0) / (h * 300.0) * 100