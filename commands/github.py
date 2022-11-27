from helpers.command import Command, Context

class Github(Command):
    def __init__(self) -> None:
        self.name = "github"
        self.help = "Returns the github link for the project."
        self.aliases = ["gh", "source"]

    async def func(self, ctx: Context) -> None:
        await ctx.send("https://github.com/spookybear0/spookybot/")