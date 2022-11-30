from helpers.command import Command, Context

class Message(Command):
    def __init__(self) -> None:
        self.name = "msg"
        self.help = "Messages somewhere"
        self.admin = True

    async def func(self, ctx: Context, location: str, message: str) -> None:
        if location.startswith("#"):
            # remember: bot accounts can't send unsolicited messages and can't send messages
            # to channels that aren't #multiplayer or #spectator
            await ctx.bot.sendMessage(location, message)
        elif location.startswith("mp_"):
            await ctx.bot.sendMessage(location, message)
        else:
            await ctx.bot.sendPM(location, message)