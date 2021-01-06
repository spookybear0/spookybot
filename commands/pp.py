import requests, asyncio

async def pp(ctx, args):
    map = args[1]
    final = ""
    r = requests.get(url=f"https://ripple.moe/letsapi/v1/pp?b={map}").json()
    pp = r["pp"]
    pp.reverse()
    for i in range(4):
        final += f" {i+97}%: {round(pp[i], 2)}pp |"
    final = r["song_name"] + " | " + final + " *" + str(r["stars"]) + " | BPM " + str(r["bpm"]) + " | AR" + str(r["ar"])
    return final

asyncio.run(pp({}, [0, 2617250]))