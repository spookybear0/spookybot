import osu_irc
from typing import Optional
from helpers.extension import Extension
from helpers.command import Context
from helpers.models import User
import tortoise

class Recommend(Extension):
    def __init__(self) -> None:
        self.name = "recommend"
        self.help = "Extension to manage saved recommendations."
        self.bot: Optional[osu_irc.Client] = None

    async def setup(self, ctx: Context) -> None:
        self.bot = ctx.bot

    async def on_message(self, ctx: Context) -> None:
        user = await User.filter(name=ctx.username).first()

        if ctx.user is None:
            return

        if user is None:
            user = await User.create(name=ctx.username, osu_id=ctx.user.user_id, rank=ctx.user.pp_rank)
        else:
            user.rank = ctx.user.pp_rank # type: ignore

        await user.save()