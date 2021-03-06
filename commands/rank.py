import aiohttp

def to_int(x):
    final = 0
    num_map = {"K":1000, "M":1000000}
    if x.isdigit():
        final = int(x)
    else:
        if len(x) > 1:
            final = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(final)

async def rank(ctx, args, test=False):
    try:
        pprank = args[1]
    except IndexError:
        return "Invalid arguments."
    
    try:
        type = args[2]
    except IndexError:
        type = None
        
    t = "pp"
    if type == "rank":
        t = "rank"
        pprank = to_int(pprank)
    elif type == "pp":
        t = "pp"
        pprank = pprank.replace("p", "")
        pprank = pprank.replace("p", "")
        pprank = to_int(pprank)
        
    else:
        try:
            pprank = int(pprank)
        except ValueError: # is str
            if pprank.endswith("pp"):
                pprank = pprank.replace("pp", "")
                pprank = to_int(pprank)
            else:
                t = "rank"
                pprank = to_int(pprank)
        else:
            try:
                pprank = pprank.replace("pp", "")
            except Exception:
                pass
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://osudaily.net/data/getPPRank.php?t={t}&v={pprank}&m=0") as r:
            text = await r.text()

    if test:
        if t == "pp":
            return int(text)
        elif t == "rank":
               return int(text)
    else:
        if t == "pp":
            return f"You need rank #{text} to have {pprank}pp."
        elif t == "rank":
            return f"You need {text}pp to be rank {args[1]} (#{pprank})."