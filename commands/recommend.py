from helpers.command import Command, Context
from helpers.extension import extension_manager
from helpers.osu import remove_non_essential_mods, mod_to_num
from extensions.np import NPExtension
from helpers.models import User
from ossapi import Cursor, RankingType, Rankings
from ossapi.models import UserStatistics
from helpers.models import Hidden
from typing import List
import random

class Recommend(Command):
    def __init__(self) -> None:
        self.name = "recommend"
        self.help = "Recommends a map for your skill level."
        self.aliases = ["r"]

        self.similar_user_attempts = 0

    async def database_similar_users(self, ctx: Context, api_user, mods, similar_user_attempts) -> None:
        cursor = Cursor(page=int(api_user.pp_country_rank)//50)
        users: List[UserStatistics] = ctx.bot.apiv2.ranking("osu", RankingType.PERFORMANCE, country=api_user.country, cursor=cursor).ranking
        # get like 10 users near the callers rank to save in the database 
        similar_country_rank_users: List[UserStatistics] = random.sample(users, 25)

        for similar_user in similar_country_rank_users:
            # if doesn't exist create
            user_ = await User.get_or_none(name=similar_user.user.username)
            if user_ is None:
                user = await User.create(name=similar_user.user.username, osu_id=similar_user.user.id, rank=int(similar_user.global_rank))
                await user.save()

        # rerun, this time with users of similar rank databased
        return await self.func(ctx, mods, similar_user_attempts+1)

    async def func(self, ctx: Context, mods: str="", similar_user_attempts: Hidden=0) -> None:
        mod_pref = mod_to_num(mods)

        user = await User.filter(name=ctx.username).first()
        api_user = await ctx.bot.api.get_user(ctx.username)

        if api_user is None:
            await ctx.send(await ctx.bot.lang.get(ctx, "error_fetching_user_data"))
            return

        if user is None:
            user = await User.create(name=ctx.username, osu_id=ctx.user.user_id, rank=ctx.user.pp_rank)

        rank_sensitivity = 1.8
        rank_variance = (user.rank**rank_sensitivity)/30000

        similar_users = await User.filter(rank__gte=user.rank-rank_variance, rank__lte=user.rank+rank_variance, id__not=user.id).all()

        if len(similar_users) == 0:
            if similar_user_attempts > 5:
                await ctx.send(await ctx.bot.lang.get(ctx, "no_similar_users_country"))
                return
            if int(api_user.pp_country_rank) <= 10000:
                if similar_user_attempts == 0:
                    await ctx.send(await ctx.bot.lang.get(ctx, "no_similar_users_database"))
                return await self.database_similar_users(ctx, api_user, mods, similar_user_attempts)

            await ctx.send(await ctx.bot.lang.get(ctx, "no_recommendation"))
            return

        bests = await ctx.bot.api.get_user_bests(ctx.user.user_id, limit=10)
        best_pps = list(map(lambda x: x.pp, bests))
        avg_pp = sum(best_pps)/len(best_pps) # avg of top 10 plays

        pp_sensitivity = 0.93

        pp_variance = 0.2*(avg_pp**pp_sensitivity)

        for similar_user in similar_users:
            if similar_user.id == user.id:
                continue

            top_plays = await ctx.bot.api.get_user_bests(similar_user.osu_id, limit=100)
            random.shuffle(top_plays)

            for play in top_plays:
                if (play.pp >= avg_pp-pp_variance and play.pp <= avg_pp+pp_variance
                and play.beatmap_id not in user.recommended_maps
                and mod_pref == remove_non_essential_mods(play.enabled_mods)):
                    np: NPExtension = extension_manager.get_extension("np")
                    ctx.message = play.beatmap_id
                    # add language support
                    msg = await np.on_message(ctx, mods=remove_non_essential_mods(play.enabled_mods))
                    await ctx.send(msg + f" | Future you: {round(play.pp, 2)}pp")

                    user.recommended_maps.append(play.beatmap_id)
                    await user.save()

                    return
        
        if int(api_user.pp_country_rank) <= 10000:
            return await self.database_similar_users(ctx, api_user, mods)
        
        await ctx.send(await ctx.bot.lang.get(ctx, "no_recommendation"))