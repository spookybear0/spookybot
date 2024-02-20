import osu_irc
from typing import Optional
from helpers.extension import Extension
from helpers.command import Context
from helpers.models import User
from osuclient.client import bancho
from osuclient.packets import constants
from osuclient.packets import rw
from osuclient.packets import builders
from helpers.config import config
from helpers.logger import logger
from helpers.extension import extension_manager
from helpers.command import command_manager
from helpers.exceptions import CommandNotFound

class Rosu(Extension):
    enabled = False
    def __init__(self) -> None:
        self.name = "rosu"
        self.help = "Extension that adds RealistikOsu! specific support."
        self.bot: Optional[osu_irc.Client] = None
        self.client: Optional[bancho.BanchoClient] = None
        self.connection: Optional[bancho.BanchoConnection] = None

    async def setup(self, ctx: Context) -> None:
        self.bot = ctx.bot

        osu = bancho.OsuVersion(year= 2022, month= 6, day= 29)
        hwid = bancho.HWIDInfo.generate_random()
        self.client = bancho.BanchoClient.new(
            version=osu,
            hwid=hwid,
        )

        res = await self.client.connect(
            config["rosu_username"],
            config["rosu_password"],
            bancho.TargetServer.from_base_url("ussr.pl")
        )

        print(res)

        ctx.bot.send = self.send

        self.start_async_thread(func=self.client.run_forever)

        self.on_message_handler = self.client.on_packet(constants.PacketID.SRV_NOTIFICATION)(self.on_message_handler)

    async def send(self, ctx: Context, message: str, user: Optional[str] = None, channel: Optional[str] = None, nodebug: bool=False) -> None:
        """
        Modified send function that sends messages to rosu instead of osu!
        """
        if ctx and not ctx.is_rosu:
            return await super().send(message, user, channel, nodebug)

        if self.testmode and user == self.test_user:
            if not nodebug:
                logger.info(f"Replied to message: {message}")
            return

        username = user
        if user:
            try:
                username = user.username
            except AttributeError:
                pass

        if not nodebug:
            logger.info(f"{username or channel} <-- {message}")

        if channel:
            await self.on_send(Context.create_event_context(self), message, channel)
        elif user:
            await self.on_send(Context.create_event_context(self), message, user)
        else:
            raise ValueError("Must specify channel or user")


    async def on_send(self, ctx: Context, message: str, target: Optional[str] = None):
        self.client.enqueue(builders.send_message_packet(message, target))
        await self.client.send()
        
    async def on_message_handler(packet: rw.PacketContext) -> None:
        print(f"Notification> {packet.reader.read_str()}")