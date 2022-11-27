from typing import Optional, List, Tuple
from helpers.extension import Extension
from helpers.command import Context, command_manager
from commands.recent import Recent
import osu_irc
import asyncio

class Watch(Extension):
    def __init__(self) -> None:
        self.name = "watch"
        self.help = "Allows watching of users recent plays."
        self.bot: Optional[osu_irc.Client] = None

        self.watched_users: dict[str, List[Tuple[str, int]]] = {}

    async def setup(self, ctx: Context) -> None:
        self.bot = ctx.bot
        self.schedule_loop(ctx)

    async def loop(self, ctx: Context) -> None:
        for user, watched in self.watched_users.items():
            for username, last_play in watched:
                recent = await ctx.api.get_user_recent(username)

                if last_play == -1:
                    self.watched_users[user][watched.index((username, last_play))] = (username, recent.beatmap_id)
                    continue

                if not recent:
                    continue

                if recent.beatmap_id != last_play:
                    ctx.username = user
                    await command_manager.get_command("recent").func(ctx, username)
                    self.watched_users[user][watched.index((username, last_play))] = (username, recent.beatmap_id)

        await asyncio.sleep(10)