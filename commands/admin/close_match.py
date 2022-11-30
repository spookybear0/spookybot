from helpers.command import Command, Context
from extensions.matchmaker import Matchmaker, Match, Lobby
import asyncio

class CloseMatch(Command):
    def __init__(self) -> None:
        self.name = "close_match"
        self.help = "Close a match"
        self.admin = True

    async def func(self, ctx: Context, mp_id: int) -> None:
        await ctx.bot.sendMessage(f"mp_{mp_id}", "!mp close")