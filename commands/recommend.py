from helpers.command import Command, Context
from helpers.extension import extension_manager
from extensions.np import NPExtension
from helpers.models import User
import random

class Recommend(Command):
    def __init__(self) -> None:
        self.name = "recommend"
        self.help = "Recommends a map for your skill level."
        self.aliases = ["r"]

    async def func(self, ctx: Context) -> None:   
        user = await User.filter(name=ctx.username).first()

        if user is None:
            user = await User.create(name=ctx.username, osu_id=ctx.user.user_id, rank=ctx.user.pp_rank)

        rank_sensitivity = 1.8
        rank_variance = (user.rank**rank_sensitivity)/30000

        similar_users = await User.filter(rank__gte=user.rank-rank_variance, rank__lte=user.rank+rank_variance, id__not=user.id).all()

        similar_users.append(User(name="FSFJ", rank=48826, osu_id=12201122))

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
                # add stuff so it doesn't recommend maps that are already recommended
                if play.pp >= avg_pp-pp_variance and play.pp <= avg_pp+pp_variance:
                    np: NPExtension = extension_manager.get_extension("np")
                    ctx.message = play.beatmap_id
                    msg = await np.on_message(ctx, mods=play.enabled_mods)
                    await ctx.send(msg + f" | Future you: {round(play.pp, 2)}pp")
                    return