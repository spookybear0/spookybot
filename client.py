from typing import Optional, Union, Tuple, Dict
from helpers.logger import logger
from helpers.config import config
from helpers.command import command_manager, Context
from helpers.extension import extension_manager
from helpers.exceptions import CommandNotFound
from helpers.osu import DictDecay
from helpers.lang import LanguageManager
import osu_irc
import ossapi
import pyosu
import os

path = os.path.dirname(os.path.realpath(__file__))

class SpookyBot(osu_irc.Client):
    # username, map_id
    recent_maps: Dict[str, str] = DictDecay(900)
    api = pyosu.OsuApi(config["osuapikey"])
    apiv2 = ossapi.OssapiV2(config["osuapiv2clientid"], config["osuapiv2key"])
    lang = LanguageManager()
    testmode = False
    test_user = None
    username = ""

    async def start(self):
        # setup
        await command_manager.init_manager(self)
        await extension_manager.init_manager(self)
        await super().start()
    
    async def stop(self):
        await extension_manager.get_extension("matchmaker").close_all_matches()
        super().stop()

    # extension hooks

    async def joinChannel(self, channel: Union[osu_irc.Channel, str]):
        await extension_manager.on_join_channel(Context.create_event_context(self), channel)
        return await super().joinChannel(channel)

    async def partChannel(self, channel: Union[osu_irc.Channel, str]):
        await extension_manager.on_part_channel(Context.create_event_context(self), channel)
        return await super().partChannel(channel)

    async def onLimit(self, payload) -> None:
        logger.warning(f"Bot is being rate limited!")
        await extension_manager.on_ratelimit(Context.create_event_context(self))
        return await super().onLimit(payload)

    async def onMemberJoin(self, channel: osu_irc.Channel, user: osu_irc.User) -> None:
        await extension_manager.on_member_join(Context.create_event_context(self), user)
        return await super().onMemberJoin(channel, user)

    async def onMemberPart(self, channel: osu_irc.Channel, user: osu_irc.User) -> None:
        await extension_manager.on_member_part(Context.create_event_context(self), user, channel)
        return await super().onMemberPart(channel, user)

    async def onMemberQuit(self, user: osu_irc.User, reason: str) -> None:
        await extension_manager.on_member_quit(Context.create_event_context(self), user, reason)
        return await super().onMemberQuit(user, reason)

    # end extension hooks

    # utility functions

    async def send(self, message: str, user: Optional[str] = None, channel: Optional[str] = None, nodebug: bool=False) -> None:
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
            await self.sendMessage(channel, message)
            await extension_manager.on_send(Context.create_event_context(self), message, channel)
        elif user:
            await self.sendPM(user, message)
            await extension_manager.on_send(Context.create_event_context(self), message, user)
        else:
            raise ValueError("Must specify channel or user")

    # end utility functions

    async def onReady(self) -> None:
        logger.info("Bot is ready!")
        await extension_manager.on_ready(Context.create_event_context(self))

    async def onReconnect(self) -> None:
        logger.warning("Bot is reconnecting!")
        await extension_manager.on_reconnect(Context.create_event_context(self))

    async def onError(self, ex: BaseException) -> None:
        logger.error(f"Bot error: {ex}")
        await extension_manager.on_error(Context.create_event_context(self), ex)
        return await super().onError(ex)

    async def onMessage(self, msg: osu_irc.Message) -> None:
        logger.debug(f"{msg.user_name} --> {msg.content}")

        user = await self.api.get_user(msg.user_name)

        await extension_manager.on_message(Context.create_event_context(self, msg, user))

        if msg.content.startswith("!mp"): # shouldn't need this since we want commands to work in multis
            return

        try:
            await command_manager.process_message(msg, user)
        except CommandNotFound:
            await self.send("Command not found!", user=user)
            return