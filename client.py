from typing import Optional
from helpers.logger import logger
from helpers.config import config
from helpers.command import command_manager
from helpers.exceptions import CommandNotFound
import osu_irc
import pyosu
import os

path = os.path.dirname(os.path.realpath(__file__))

class SpookyBot(osu_irc.Client):
    api = pyosu.OsuApi(config["osuapikey"])
    testmode = False
    
    async def send(self, message: str, channel: Optional[str] = None, user: Optional[str] = None) -> None:
        if self.testmode:
            logger.debug(f"Replied to message: {message}")
            return

        if channel:
            await self.sendMessage(channel, message)
        elif user:
            await self.sendPM(user, message)
        else:
            raise ValueError("Must specify channel or user")

    async def onReady(self) -> None:
        logger.info("Bot is ready!")

    async def onReconnect(self) -> None:
        logger.warning("Bot is reconnecting!")

    async def onError(self, ex: BaseException) -> None:
        logger.error(f"Bot error: {ex}")
        return await super().onError(ex)

    async def onMessage(self, msg: osu_irc.Message) -> None:
        logger.debug(f"Message received: {msg.content}")
        user = await self.api.get_user(msg.user_name)
        try:
            await command_manager.process_message(msg, user)
        except CommandNotFound:
            return await self.send("Command not found!", user=user)