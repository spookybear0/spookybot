from typing import Dict, Optional, Callable, List, Type, Union
from collections.abc import KeysView, ValuesView
from typing_extensions import Self
from helpers.command import Context
from helpers.logger import logger
import osu_irc

class Extension:
    # default values
    name: str = ""
    func: Optional[Callable] = None
    help: str = ""
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
        return f"{self.__class__.__name__}({self.name}, {self.func}, {self.help})"

    def __str__(self):
        return repr(self)

    def shared_instance(self) -> Self:
        return extension_manager[self.name]

    async def setup(self, ctx: Context):
        pass

    async def on_message(self, ctx: Context):
        pass

    async def on_reconnect(self, ctx: Context):
        pass

    async def on_ready(self, ctx: Context):
        pass

    async def on_error(self, ctx: Context, error: BaseException):
        pass

    async def on_join_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        pass

    async def on_part_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        pass

    async def on_ratelimit(self, ctx: Context):
        pass

    async def on_member_join(self, ctx: Context, user: osu_irc.User):
        pass

    async def on_member_part(self, ctx: Context, user: osu_irc.User, channel: osu_irc.Channel):
        pass

    async def on_member_quit(self, ctx: Context, user: osu_irc.User, reason: str):
        pass

class ExtensionManager:
    def __init__(self, bot=None) -> None:
        self.bot = bot
        self.extensions: Dict[str, Extension] = {}

    async def init_manager(self, bot):
        self.bot = bot
        await self.register_all_extensions()

    def register(self, extension: Type[Extension]) -> Extension:
        ext: Extension = extension()
        logger.debug(f"Registering extension {ext.name}")
        self.extensions[ext.name] = ext # initalize class
        return ext

    def unregister(self, ext) -> None:
        del self.extensions[ext.name]

    def get_all(self) -> ValuesView[Extension]:
        return self.extensions.values()

    def get_all_names(self) -> KeysView[str]:
        return self.extensions.keys()

    def get_extension(self, name: str) -> Optional[Extension]:
        if name in self.extensions:
            return self.extensions[name]
        return None

    async def on_message(self, ctx: Context):
        logger.debug(f"EVENT on_message({ctx.message})")
        for ext in self.extensions.values():
            await ext.on_message(ctx)

    async def on_reconnect(self, ctx: Context):
        logger.debug("EVENT on_reconnect()")
        for ext in self.extensions.values():
            await ext.on_reconnect(ctx)

    async def on_ready(self, ctx: Context):
        logger.debug("EVENT on_ready()")
        for ext in self.extensions.values():
            await ext.on_ready(ctx)

    async def on_error(self, ctx: Context, error: BaseException):
        logger.debug(f"EVENT on_error({error})")
        for ext in self.extensions.values():
            await ext.on_error(ctx, error)

    async def on_join_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        logger.debug(f"EVENT on_join_channel({channel})")
        for ext in self.extensions.values():
            await ext.on_join_channel(ctx, channel)

    async def on_part_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        logger.debug(f"EVENT on_part_channel({channel})")
        for ext in self.extensions.values():
            await ext.on_part_channel(ctx, channel)

    async def on_ratelimit(self, ctx: Context):
        logger.debug("EVENT on_ratelimit()")
        for ext in self.extensions.values():
            await ext.on_ratelimit(ctx)

    async def on_member_join(self, ctx: Context, user: osu_irc.User):
        for ext in self.extensions.values():
            await ext.on_member_join(ctx, user)

    async def on_member_part(self, ctx: Context, user: osu_irc.User, channel: osu_irc.Channel):
        for ext in self.extensions.values():
            await ext.on_member_part(ctx, user, channel)

    async def on_member_quit(self, ctx: Context, user: osu_irc.User, reason: str):
        for ext in self.extensions.values():
            await ext.on_member_quit(ctx, user, reason)

    # add more handlers

    async def register_all_extensions(self):
        import extensions
        for ext in dir(extensions):
            if not ext.startswith("_"):
                ext_class = getattr(extensions, ext)
                if type(ext_class) == type and Extension in ext_class.__bases__:
                    registered_ext = self.register(ext_class)
                    await registered_ext.setup(Context.create_event_context(self.bot))

        logger.info("All extension registered")

extension_manager = ExtensionManager()