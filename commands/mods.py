from helpers.extension import extension_manager
from helpers.command import Command, Context
from helpers.osu import mod_to_num
from extensions.np import NPExtension


class Mods(Command):
    def __init__(self) -> None:
        self.name = "mods"
        self.help = "Calculates the pp most recent map would give with the given mods."
        self.aliases = ["with"]

    async def func(self, ctx: Context, mods: str) -> None:
        #return await ctx.send("Not implemented!")

        mods = mod_to_num(mods)
        np: NPExtension = extension_manager.get_extension("np")
        try:
            ctx.message = ctx.bot.recent_maps[ctx.username]
        except KeyError:
            await ctx.send(await ctx.bot.lang.get(ctx, "no_recent_map"))
            return

        msg = await np.on_message(ctx, mods=mods)
        await ctx.send(msg)