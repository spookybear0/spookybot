from helpers.command import Command, Context
from helpers.config import config
from helpers.models import User

class AddUser(Command):
    def __init__(self) -> None:
        self.name = "add_user"
        self.help = "Adds a user to a database"
        self.admin = True

    async def func(self, ctx: Context, username: str) -> None:
        user = await config["bot"].api.get_user(username)
        if user is None:
            await ctx.send("User not found")
            return

        db_user = await User.filter(osu_id=user.user_id).first()
        if db_user is not None:
            await ctx.send("User already exists in database")
            return

        await User.update_or_create(name=username, osu_id=user.user_id, rank=user.pp_rank)
        await ctx.send(f"Added user {username} to database")