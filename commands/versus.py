from helpers.command import Command, Context
from helpers.extension import extension_manager
from extensions import Matchmaker

class Versus(Command):
    def __init__(self) -> None:
        self.name = "versus"
        self.help = "1v1s a user"

    async def func(self, ctx: Context, other_user: str) -> None:
        matchmaker: Matchmaker = extension_manager.get_extension("matchmaker")
        return await matchmaker.match(ctx, await ctx.bot.api.get_user(other_user))