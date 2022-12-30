from helpers.command import Command, Context

class Recommend(Command):
    def __init__(self) -> None:
        self.name = "recommend"
        self.help = "Recommends a map for your skill level."

    async def func(self, ctx: Context) -> None:
        await ctx.send("Not implemented!")
        return
        