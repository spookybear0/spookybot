from helpers.extension import extension_manager
from helpers.command import Command, Context
from extensions.watch import Watch as WatchExtension
from typing import Optional


class Unwatch(Command):
    def __init__(self) -> None:
        self.name = "unwatch"
        self.help = "Stops messaging you a users recent plays."
        self.aliases = ["uw"]

    async def setup(self, ctx: Context) -> None:
        self.watch_ext: WatchExtension = extension_manager.get_extension("watch")

    async def func(self, ctx: Context, username: Optional[str]=None) -> None:
        # TODO urgent: fix this, it's broken
        if self.watch_ext is None:
            self.watch_ext: WatchExtension = extension_manager.get_extension("watch")

        user_arg = True
        if username is None:
            username = ctx.username
            user_arg = False
        
        if self.watch_ext.watched_users.get(ctx.username) is not None:
            for user, last_play in self.watch_ext.watched_users[ctx.username]:
                if username == user:
                    self.watch_ext.watched_users[ctx.username].remove((user, last_play))
                    if user_arg:
                        return await ctx.send(await ctx.bot.lang.get(ctx, "stopped_watching", username))
                    else:
                        return await ctx.send(await ctx.bot.lang.get(ctx, "stopped_watching_self"))
            
            if user_arg:
                return await ctx.send(await ctx.bot.lang.get(ctx, "not_watching", username))
            else:
                return await ctx.send(await ctx.bot.lang.get(ctx, "not_watching_self"))
        else:
            return await ctx.send(await ctx.bot.lang.get(ctx, "not_watching", username))