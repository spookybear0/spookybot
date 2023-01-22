from typing import Optional
from helpers.command import Command, Context, command_manager

class User(Command):
    def __init__(self) -> None:
        self.name = "user"
        self.help = "Gets info about a user."
        self.aliases = ["u", "osu", "standard", "taiko", "ctb", "mania"]

        self.modes = {
            "standard": 0,
            "taiko": 1,
            "ctb": 2,
            "mania": 3,
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3
        }

        self.num_to_mode = {
            0: "standard",
            1: "taiko",
            2: "ctb",
            3: "mania"
        }

    async def func(self, ctx: Context, username: Optional[str]=None, mode: str="standard") -> None:
        if not username:
            username = ctx.username
        if username in self.modes.keys(): # if username is a mode
            return await ctx.send(await ctx.bot.lang.get(ctx, "username_not_mode", command_manager.prefix, username))

        mode_num = self.modes.get(ctx.command_name) # try with command name

        if mode_num is None:
            mode_num = self.modes.get(mode, None) # try with mode arg

        if mode_num is None:
            return await ctx.send(await ctx.bot.lang.get(ctx, "invalid_mode"))

        user = await ctx.bot.api.get_user(username, mode_num)

        if not user:
            return await ctx.send(await ctx.bot.lang.get(ctx, "user_not_found"))

        return await ctx.send(await ctx.bot.lang.get(ctx, "user_info", self.num_to_mode[mode_num], username, user.pp_raw, user.pp_rank, user.pp_country_rank, user.country))