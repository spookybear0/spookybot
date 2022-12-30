from helpers.command import Command, Context
from extensions.matchmaker import Matchmaker, Match, Lobby
import asyncio

class CreateMatch(Command):
    def __init__(self) -> None:
        self.name = "create_match"
        self.help = "Creates a match"
        self.admin = True

    async def func(self, ctx: Context) -> None:
        matchmaker: Matchmaker = Matchmaker().shared_instance()
        match_: Match = await matchmaker.match(ctx, ctx.username)