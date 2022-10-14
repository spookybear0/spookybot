from typing import Dict, Optional, Callable, List, Type, Union
from collections.abc import KeysView, ValuesView
from helpers.command import Context
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

    async def on_member_part(self, ctx: Context, user: osu_irc.User):
        pass

    async def on_member_quit(self, ctx: Context, user: osu_irc.User, reason: str):
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

    async def on_message(self, ctx: Context):
        for ext in self.extensions.values():
            await ext.on_message(ctx)

    async def on_reconnect(self, ctx: Context):
        for ext in self.extensions.values():
            await ext.on_reconnect(ctx)

    async def on_ready(self, ctx: Context):
        for ext in self.extensions.values():
            await ext.on_ready(ctx)

    async def on_error(self, ctx: Context, error: BaseException):
        for ext in self.extensions.values():
            await ext.on_error(ctx, error)

    async def on_join_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        for ext in self.extensions.values():
            await ext.on_join_channel(ctx, channel)

    async def on_part_channel(self, ctx: Context, channel: Union[osu_irc.Channel, str]):
        for ext in self.extensions.values():
            await ext.on_part_channel(ctx, channel)

    async def on_ratelimit(self, ctx: Context):
        for ext in self.extensions.values():
            await ext.on_ratelimit(ctx)

    async def on_member_join(self, ctx: Context, user: osu_irc.User, channel: osu_irc.Channel):
        for ext in self.extensions.values():
            await ext.on_member_join(ctx, user, channel)

    async def on_member_part(self, ctx: Context, user: osu_irc.User, channel: osu_irc.Channel):
        for ext in self.extensions.values():
            await ext.on_member_part(ctx, user, channel)

    async def on_member_quit(self, ctx: Context, user: osu_irc.User, reason: str):
        for ext in self.extensions.values():
            await ext.on_member_quit(ctx, user, reason)

    # add more handlers

    def register_all_extensions(self):
        import extensions
        for ext in dir(extensions):
            if not ext.startswith("_"):
                ext_class = getattr(extensions, ext)
                if type(ext_class) == type and Extension in ext_class.__bases__:
                    self.register(ext_class)

extension_manager = ExtensionManager()