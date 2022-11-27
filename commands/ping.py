from helpers.command import Command, Context

class Ping(Command):
    def __init__(self) -> None:
        self.name = "ping"
        self.help = "Checks if bot is online and returns ping"

    async def func(self, ctx: Context) -> None:
        await ctx.send("Pong!")