from helpers.extension import extension_manager
from helpers.command import Command, Context
from extensions.watch import Watch as WatchExtension
from typing import Optional


class Watch(Command):
    def __init__(self) -> None:
        self.name = "watch"
        self.help = "Messages you a users recent plays."
        self.aliases = ["w"]

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
                if user_arg:
                    return await ctx.send(f"Already watching {username}, did you mean to use !unwatch?")
                else:
                    return await ctx.send("Already watching your recent plays, did you mean to use !unwatch?")

            self.watch_ext.watched_users[ctx.username].append((username, -1))
        else:
            self.watch_ext.watched_users[ctx.username] = [(username, -1)]

        if user_arg:
            return await ctx.send(f"Now watching {username}.")
        else:
            return await ctx.send(f"Now watching your recent plays.")