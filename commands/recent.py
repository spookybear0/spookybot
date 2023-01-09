from helpers.command import Command, Context
from helpers.osu import num_to_mod, acc_calc, py_oppai
import os

class Recent(Command):
    def __init__(self) -> None:
        self.name = "recent"
        self.help = "Returns recent plays of a user"
        self.aliases = ["rs", "replay", "last"]

    async def func(self, ctx: Context, username: str=None, mode: int=0, watch=False) -> None:
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
        pp_for_fc = await py_oppai(recent.beatmap_id, [acc], mods=recent.enabled_mods, misses=0, combo=map.max_combo)
        pp_for_fc = round(pp_for_fc["pp"][0], 2)
        if recent.rank == "F":
            try:
                pp = await py_oppai(recent.beatmap_id, [acc], mods=recent.enabled_mods, misses=recent.misses, combo=recent.maxcombo, fc=recent.perfect)
                pp = pp["pp"]
            except Exception:
                pp = 0 # unavailable pp (probably failed or something)
        else: 
            score = await ctx.api.get_score(map.beatmap_id, user=username)
            pp = round(float(score.pp), 2)
        
        mods = "".join(num_to_mod(recent.enabled_mods))

        if mods:
            mods = f" +{mods}"

        resp = f"{username} | {map.artist} - {map.title} [{map.version}]{mods} {round(acc, 2)}% {round(map.difficultyrating, 2)}* " \
            f"| {recent.rank} | {pp}pp | {pp_for_fc}pp if FC | {recent.maxcombo}x | {recent.countmiss}x miss{perfect}"
        
        if watch:
            resp += " | use !unwatch to stop watching"

        return await ctx.send(resp)