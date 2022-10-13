from typing import Dict, Optional, Callable, List, Type, Union
from collections.abc import KeysView, ValuesView
from helpers.logger import logger
import osu_irc

class Extension:
    # default values
    name = None
    func = None
    help = None
    aliases: List[str] = []

    @staticmethod
    def create_extension(cls, name: str, func: Callable, help: Optional[str] = None, aliases: List[str] = []):
        """
        Creates a extension object dynamically. This should not be used under normal circumstances.
        """
        cmd = cls()
        cmd.name = name
        cmd.func = func
        cmd.help = help
        cmd.aliases = aliases
        return cmd

    def __call__(self, context, *args, **kwargs):
        return self.func(context, *args, **kwargs)

    def __repr__(self):
        return f"Extension({self.name}, {self.func}, {self.help})"

    def __str__(self):
        return self.name

    async def on_message(self, message: osu_irc.Message, user):
        pass

    async def on_reconnect(self):
        pass

    async def on_ready(self):
        pass

    async def on_error(self, error: BaseException):
        pass

    async def on_join_channel(self, channel: Union[osu_irc.Channel, str]):
        pass

    async def on_part_channel(self, channel: Union[osu_irc.Channel, str]):
        pass

    async def on_ratelimit(self):
        pass

    async def on_member_join(self, user: osu_irc.User):
        pass

    async def on_member_part(self, user: osu_irc.User):
        pass

    async def on_member_quit(self, user: osu_irc.User, reason: str):
        pass

class ExtensionManager:
    def __init__(self, bot=None) -> None:
        self.bot = bot
        self.extensions: Dict[str, Extension] = {}

    def init_manager(self, bot):
        self.bot = bot
        self.register_all_extensions()

    def register(self, extension: Type[Extension]) -> None:
        ext = extension()
        logger.debug(f"Registering extension {ext.name}")
        self.extensions[ext.name] = ext # initalize class

    def unregister(self, ext) -> None:
        del self.extensions[ext.name]

    def get_all(self) -> ValuesView[Extension]:
        return self.extensions.values()

    def get_all_names(self) -> KeysView[str]:
        return self.extensions.keys()

    def get_extensions(self, name: str) -> Optional[Extension]:
        if name in self.extensions:
            return self.extensions[name]
        return None

    async def on_message(self, message: osu_irc.Message, user):
        logger.debug(f"EVENT on_message({message}, {user})")
        for ext in self.extensions.values():
            await ext.on_message(message, user)

    async def on_reconnect(self):
        logger.debug("EVENT on_reconnect()")
        for ext in self.extensions.values():
            await ext.on_reconnect()

    async def on_ready(self):
        logger.debug("EVENT on_ready()")
        for ext in self.extensions.values():
            await ext.on_ready()

    async def on_error(self, error: BaseException):
        logger.debug(f"EVENT on_error({error})")
        for ext in self.extensions.values():
            await ext.on_error(error)

    async def on_join_channel(self, channel: Union[osu_irc.Channel, str]):
        logger.debug(f"EVENT on_join_channel({channel})")
        for ext in self.extensions.values():
            await ext.on_join_channel(channel)

    async def on_part_channel(self, channel: Union[osu_irc.Channel, str]):
        logger.debug(f"EVENT on_part_channel({channel})")
        for ext in self.extensions.values():
            await ext.on_part_channel(channel)

    async def on_ratelimit(self):
        logger.debug("EVENT on_ratelimit()")
        for ext in self.extensions.values():
            await ext.on_ratelimit()

    async def on_member_join(self, channel: osu_irc.Channel, user: osu_irc.User):
        for ext in self.extensions.values():
            await ext.on_member_join(channel, user)

    async def on_member_part(self, channel: osu_irc.Channel, user: osu_irc.User):
        for ext in self.extensions.values():
            await ext.on_member_part(channel, user)

    async def on_member_quit(self, user: osu_irc.User, reason: str):
        for ext in self.extensions.values():
            await ext.on_member_quit(user, reason)

    # add more handlers

    def register_all_extensions(self):
        import extensions
        for ext in dir(extensions):
            if not ext.startswith("_"):
                ext_class = getattr(extensions, ext)
                if type(ext_class) == type and Extension in ext_class.__bases__:
                    self.register(ext_class)

        logger.info("All extension registered")

extension_manager = ExtensionManager()