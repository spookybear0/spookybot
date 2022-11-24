from helpers.extension import extension_manager
from helpers.command import Command, Context
from extensions.np import NPExtension


# TODO: add a way to use !acc with !mods
class Acc(Command):
    def __init__(self) -> None:
        self.name = "acc"
        self.help = "Calculates the pp most recent map would give with the given accuracy."
        self.aliases = ["accuracy"]

    async def func(self, ctx: Context, acc: float):
        # not implemented since ripple api breaks with specific accs
        return await ctx.send("Not implemented!")
        np: NPExtension = extension_manager.get_extension("np")

        ctx.message = ctx.bot.recent_maps[ctx.username]

        await np.on_message(ctx, acc=acc)