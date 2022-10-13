from typing import Optional, Union
from helpers.logger import logger
from helpers.config import config
from helpers.command import command_manager
from helpers.extension import extension_manager
from helpers.exceptions import CommandNotFound
import osu_irc
import pyosu
import os

path = os.path.dirname(os.path.realpath(__file__))

class SpookyBot(osu_irc.Client):
    api = pyosu.OsuApi(config["osuapikey"])
    testmode = False

    # extension hooks

    async def joinChannel(self, channel: Union[osu_irc.Channel, str]):
        await extension_manager.on_join_channel(channel)
        return await super().joinChannel(channel)

    async def partChannel(self, channel: Union[osu_irc.Channel, str]):
        await extension_manager.on_part_channel(channel)
        return await super().partChannel(channel)

    async def onLimit(self, payload) -> None:
        logger.warning(f"Bot is being rate limited!")
        await extension_manager.on_ratelimit()
        return await super().onLimit(payload)

    # end extension hooks

    # utility functions

    async def send(self, message: str, user: Optional[str] = None, channel: Optional[str] = None) -> None:
        if self.testmode:
            logger.debug(f"Replied to message: {message}")
            return

        if channel:
            await self.sendMessage(channel, message)
        elif user:
            await self.sendPM(user, message)
        else:
            raise ValueError("Must specify channel or user")

    # end utility functions

    async def onReady(self) -> None:
        command_manager.init_manager(self)
        extension_manager.init_manager(self)
        logger.info("Bot is ready!")
        await extension_manager.on_ready()

    async def onReconnect(self) -> None:
        logger.warning("Bot is reconnecting!")
        await extension_manager.on_reconnect()

    async def onError(self, ex: BaseException) -> None:
        logger.error(f"Bot error: {ex}")
        await extension_manager.on_error(ex)
        return await super().onError(ex)

    async def onMessage(self, msg: osu_irc.Message) -> None:
        logger.debug(f"Message received: {msg.content}")

        user = await self.api.get_user(msg.user_name)

        await extension_manager.on_message(msg, user)

        try:
            await command_manager.process_message(msg, user)
        except CommandNotFound:
            return await self.send("Command not found!", user=user)