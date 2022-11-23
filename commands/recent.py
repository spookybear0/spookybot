from helpers.command import Command, Context
from helpers.osu import num_to_mod, acc_calc, py_oppai
import os

class Recent(Command):
    def __init__(self) -> None:
        self.name = "recent"
        self.help = "Returns recent plays of a user"
        self.aliases = ["rs", "replay", "last"]

    async def func(self, ctx: Context, username: str=None, mode: int=0):
        if username is None:
            username = ctx.username

        recent = await ctx.api.get_user_recent(username, mode, "string")

        if recent is None:
            return await ctx.send(f'No recent plays found for "{username}"')

        map = await ctx.api.get_beatmap(beatmap_id=recent.beatmap_id)

        ctx.bot.recent_maps[ctx.username] = recent.beatmap_id

        acc = acc_calc(recent.count300, recent.count100, recent.count50, recent.countmiss)
        perfect = ""
        if not recent.perfect:
            perfect = " | PERFECT"
        # pp calc
        if recent.rank == "F":
            try:
                pp = await py_oppai(recent.map_id, acc, mods=recent.mods, misses=recent.misses, combo=recent.maxcombo, fc=recent.perfect)["pp"]
            except Exception:
                pp = "unavailable "
        else: 
            score = await ctx.api.get_score(map.beatmap_id, user=username)
            pp = round(float(score.pp), 2)
        
        mods = "".join(num_to_mod(recent.enabled_mods))

        if mods:
            mods = f" +{mods}"
        
        return await ctx.send(f"{username} | {map.artist} - {map.title} [{map.version}]{mods} {round(acc, 2)}% {round(map.difficultyrating, 2)}* " \
            f"| {recent.rank} | {pp}pp | {int(recent.score)} | {recent.maxcombo}x | {recent.count300}x 300, {recent.count100}x 100, " \
            f"{recent.count50}x 50, {recent.countmiss}x miss{perfect}"
        )