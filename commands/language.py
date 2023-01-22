from helpers.command import Command, Context
from helpers.models import User

aliases = {
    "english": "en",
    "eng": "en",
    "tsundere": "tsu",
    "catboy": "cat",
    "catgirl": "cat",
    "uwu": "cat",
}

class Language(Command):
    def __init__(self) -> None:
        self.name = "langauge"
        self.help = "Changes the language of the bot."
        self.aliases = ["lang"]

    async def func(self, ctx: Context, lang: str) -> None:
        lang = lang.lower()

        if lang in aliases:
            lang = aliases[lang]

        if lang not in ctx.bot.lang.language_pack.keys():
            return await ctx.send(await ctx.bot.lang.get(ctx, "invalid_language"))

        user = await User.get(name=ctx.username)
        user.language = lang
        await user.save()

        return await ctx.send(await ctx.bot.lang.get(ctx, "language_changed", lang))