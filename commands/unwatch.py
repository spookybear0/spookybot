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
        if self.watch_ext is None:
            self.watch_ext: WatchExtension = extension_manager.get_extension("watch")

        user_arg = True
        if username is None:
            username = ctx.username
            user_arg = False
        
        if self.watch_ext.watched_users.get(ctx.username):
            if username in self.watch_ext.watched_users[ctx.username]:
                self.watch_ext.watched_users[ctx.username].remove(username)
                if user_arg:
                    return await ctx.send(f"Stopped watching {username}.")
                else:
                    return await ctx.send("Stopped watching your recent plays.")
            
            if user_arg:
                return await ctx.send(f"You are not watching {username}, did you mean to use !watch?")
            else:
                return await ctx.send("You are not watching your recent plays, did you mean to use !watch?")
        else:
            return await ctx.send(f"You are not watching {username}.")