import requests

def to_int(x):
    final = 0
    num_map = {"K":1000, "M":1000000, "B":1000000000}
    if x.isdigit():
        final = int(x)
    else:
        if len(x) > 1:
            final = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(final)

async def rank(ctx, args):
    try:
        pprank = args[1]
    except IndexError:
        return "Invalid arguments."
    t = "pp"
    try:
        pprank = int(pprank)
    except ValueError: # is str
        t = "rank"
        pprank = to_int(pprank)
    else:
        try:
            pprank = pprank.replace("p", "")
            pprank = pprank.replace("p", "")
        except Exception:
            pass
    r = requests.get(f"https://osudaily.net/data/getPPRank.php?t={t}&v={pprank}&m=0")
    if t == "pp":
        return f"You need {pprank}pp to be #{r.text}."
    elif t == "rank":
        return f"You need {r.text}pp to be {args[1]} (#{pprank})."