from helpers.command import Command, Context
from helpers.logger import logger, OsuDebugHandler
import logging

class Debug(Command):
    def __init__(self) -> None:
        self.name = "debug"
        self.help = "Turns on debug mode"
        self.admin = True
        self.aliases = ["dbg"]

    async def func(self, ctx: Context) -> None:
        for filter in logger.filters:
            if isinstance(filter, OsuDebugHandler):
                logger.removeFilter(filter)
                await ctx.send(await ctx.bot.lang.get(ctx, "debug_disabled"))
                logger.setLevel(logging.INFO)
                return
        
        logger.addHandler(OsuDebugHandler())
        logger.setLevel(logging.DEBUG)
        await ctx.send(await ctx.bot.lang.get(ctx, "debug_enabled"))