from helpers.command import Command, Context
from helpers.extension import extension_manager
import asyncio

class CloseAllMatches(Command):
    def __init__(self) -> None:
        self.name = "close_all_matches"
        self.help = "Close all matches"
        self.admin = True

    async def func(self, ctx: Context, mp_id: int) -> None:
        await extension_manager.get_extension("matchmaker").close_all_matches()
        await ctx.send(await ctx.bot.lang.get(ctx, "all_matches_closed"))