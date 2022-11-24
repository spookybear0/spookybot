from helpers.command import Command, Context

class Info(Command):
    def __init__(self) -> None:
        self.name = "info"
        self.help = "Gets info about the bot."

    async def func(self, ctx: Context):
        await ctx.send("Github: https://github.com/spookybear0/spookybot.")
        # add more