from helpers.command import Command, Context
import asyncio
import os

class Restart(Command):
    def __init__(self) -> None:
        self.name = "restart"
        self.help = "Restarts the bot"
        self.admin = True

    async def func(self, ctx: Context) -> None:
        await ctx.send("Restarting...")
        os.system("sudo service restart spookybot") # is this safe?