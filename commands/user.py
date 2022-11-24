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

    async def func(self, ctx: Context, username: Optional[str]=None, mode: str="standard"):
        if not username:
            username = ctx.username
        if username in self.modes.keys(): # if username is a mode
            return await ctx.send(f"Username cannot be a mode, use {command_manager.prefix}{username} instead.")

        mode_num = self.modes.get(ctx.command_name) # try with command name

        if mode_num is None:
            mode_num = self.modes.get(mode, None) # try with mode arg

        if mode_num is None:
            return await ctx.send("Invalid mode!")

        user = await ctx.bot.api.get_user(username, mode_num)

        if not user:
            return await ctx.send("User not found!")

        return await ctx.send(f"In {self.num_to_mode[mode_num]}, {username} has {user.pp_raw}pp and is rank #{user.pp_rank} globally and #{user.pp_country_rank} rank in {user.country}.")