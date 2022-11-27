from helpers.command import Command, Context
from typing import Union
import aiohttp

def to_int(x) -> int:
    final = 0
    num_map = {"K": 1000, "M": 1000000}
    if x.isdigit():
        final = int(x)
    else:
        if len(x) > 1:
            final = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(final)


class Rank(Command):
    def __init__(self) -> None:
        self.name = "rank"
        self.help = "Converts between the rank of a user and their pp"

    async def func(self, ctx: Context, value: Union[int, str], type_: str=None) -> None:
        if type_ == "rank":
            ret = to_int(value.replace("#", ""))
        elif type_ == "pp":
            ret = to_int(value.replace("p", ""))
        else:
            if value.endswith("pp"):
                type_ = "pp"
                ret = to_int(value.replace("p", ""))
            elif value.startswith("#"):
                type_ = "rank"
                ret = to_int(value.replace("#", ""))
            else:
                return await ctx.send('Invalid type. Value must start with "#", end with "pp", or the value type must be specified with "rank" or "pp".')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://osudaily.net/data/getPPRank.php?t={type_}&v={ret}&m=0") as r:
                text = await r.text()

        if type_ == "pp":
            return await ctx.send(f"You need rank #{text} to have {ret}pp.")
        elif type_ == "rank":
            return await ctx.send(f"You need {text}pp to be rank {value} (#{ret}).")