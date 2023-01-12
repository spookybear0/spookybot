from helpers.command import Command, Context
from helpers.config import config
import os

class Restart(Command):
    def __init__(self) -> None:
        self.name = "restart"
        self.help = "Restarts the bot"
        self.admin = True

    async def func(self, ctx: Context) -> None:
        await ctx.send("Restarting...")
        os.system(f'echo "{config["root_password"]}\n" | sudo -S service restart spookybot') # is this safe?