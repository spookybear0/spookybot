from helpers.command import Command, Context
from helpers.logger import logger, OsuDebugHandler

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
                await ctx.send("Debug mode disabled!")
                return
        
        logger.addHandler(OsuDebugHandler())
        await ctx.send("Debug mode enabled!")