import requests

def pp(map):
    final = ""
    r = requests.get(url=f"https://osu.spookybear.xyz/letsapi/v1/pp?b={map}").json()
    print(r)
    pp = r["pp"]
    for i in range(4):
        j = i+1
        final += f" {i+97}%: {pp[i]}pp |"
    final = r["song_name"] + " | " + final + " *" + str(r["stars"]) + " | BPM " + str(r["bpm"]) + " | AR" + str(r["ar"])
    return final