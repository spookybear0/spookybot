from enum import Enum
from typing import Dict, List, Optional
from helpers.extension import Extension, extension_manager
from helpers.command import Context
import osu_irc
import pyosu

class MatchType(Enum):
    """The type of match to create."""
    SINGLES = 0
    DOUBLES = 1

class Lobby:
    """A lobby for a match."""
    @classmethod
    async def create(cls, id: int, password: str):
        self = cls()

        self.id: int = id
        self.password: str = ""
        self.bot = extension_manager.bot # shared bot

        await self.bot.joinChannel(f"mp_{self.id}")

        await self.set_password(password)

        return self

    async def send_message(self, message: str):
        await self.bot.sendMessage(f"mp_{self.id}", message)

    async def invite(self, member: pyosu.models.User | str):
        if isinstance(member, pyosu.models.User):
            await self.send_message(f"!mp invite {member.username}")
        else:
            await self.send_message(f"!mp invite {member}")

    def create_invite_link(self):
        return f"[osump://{self.id}/ Invite Link]"

    async def close(self):
        await self.send_message("!mp close")

    async def set_password(self, password: str):
        self.password = password
        if password == "":
            await self.send_message("!mp password")
        else:
            await self.send_message(f"!mp password {password}")

    async def move(self, username: str, slot: int):
        await self.send_message(f"!mp move {username} {slot}")

    async def on_message(self, ctx: Context):
        print(ctx.content)

class Match:
    def __init__(self, type: MatchType, members: List[pyosu.models.User]) -> None:
        self.type: MatchType = type
        self.members: List[pyosu.models.User] = members
        self.creator: pyosu.models.User = members[0]
        self.lobby: Optional[Lobby] = None

    async def create_lobby(self, name: str="Matchmaking Lobby") -> Lobby:
        bancho_bot: Extension = extension_manager.get_extension("banchobot")
        self.lobby: Lobby = await bancho_bot.mp_make(name)
        for member in self.members:
            await self.lobby.invite(member)
        return self.lobby

class Matchmaker(Extension):
    def __init__(self) -> None:
        self.name = "matchmaker"
        self.help = "Matchmaking extension."
        self.bot: Optional[osu_irc.Client] = None

    async def setup(self, ctx: Context) -> None:
        self.bot = ctx.bot
        self.matches: List = []

    async def close_all_matches(self) -> None:
        for match in self.matches:
            await match.lobby.close()

    async def match(self, ctx: Context, other_user: pyosu.models.User, name: str="Matchmaking Lobby") -> Match:
        match = Match(MatchType.SINGLES, [ctx.user, other_user])
        self.matches.append(match)

        await match.create_lobby(name)
        
        return match

    async def on_message(self, ctx: Context) -> None:
        for match_ in self.matches:
            if match_.lobby and f"mp_{match_.lobby.id}" == str(ctx.channel):
                await match_.lobby.on_message(ctx)