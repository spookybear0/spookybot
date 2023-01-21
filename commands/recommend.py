from helpers.command import Command, Context
from helpers.extension import extension_manager
from helpers.osu import remove_non_essential_mods, mod_to_num
from extensions.np import NPExtension
from helpers.models import User
import random

class Recommend(Command):
    def __init__(self) -> None:
        self.name = "recommend"
        self.help = "Recommends a map for your skill level."
        self.aliases = ["r"]

    async def func(self, ctx: Context, mods: str="") -> None:
        mod_pref = mod_to_num(mods)

        user = await User.filter(name=ctx.username).first()

        if user is None:
            user = await User.create(name=ctx.username, osu_id=ctx.user.user_id, rank=ctx.user.pp_rank)

        rank_sensitivity = 1.8
        rank_variance = (user.rank**rank_sensitivity)/30000

        similar_users = await User.filter(rank__gte=user.rank-rank_variance, rank__lte=user.rank+rank_variance, id__not=user.id).all()

        if len(similar_users) == 0:
            await ctx.send("No recommendations found for your rank! This could be because you're too far away from the nearest ranked person who uses this bot.")
            return

        bests = await ctx.api.get_user_bests(ctx.user.user_id, limit=10)
        best_pps = list(map(lambda x: x.pp, bests))
        avg_pp = sum(best_pps)/len(best_pps) # avg of top 10 plays

        pp_sensitivity = 0.93

        pp_variance = 0.2*(avg_pp**pp_sensitivity)

        for similar_user in similar_users:
            top_plays = await ctx.api.get_user_bests(similar_user.osu_id, limit=100)
            random.shuffle(top_plays)

            for play in top_plays:
                if (play.pp >= avg_pp-pp_variance and play.pp <= avg_pp+pp_variance
                and play.beatmap_id not in user.recommended_maps
                and mod_pref == remove_non_essential_mods(play.enabled_mods)):
                    np: NPExtension = extension_manager.get_extension("np")
                    ctx.message = play.beatmap_id
                    msg = await np.on_message(ctx, mods=remove_non_essential_mods(play.enabled_mods))
                    await ctx.send(msg + f" | Future you: {round(play.pp, 2)}pp")

                    user.recommended_maps.append(play.beatmap_id)
                    await user.save()

                    return

        await ctx.send("No recommendations found for your rank! This could be because you're too far away from the nearest ranked person who uses this bot.")