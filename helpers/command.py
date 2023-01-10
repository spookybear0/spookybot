from typing import Any, Dict, Optional, Callable, List, Type
from helpers.exceptions import CommandNotFound
from typing_extensions import Self
from helpers.logger import logger
import inspect
import osu_irc
import pyosu

class Context:
    def __init__(self) -> None:
        """
        Internal method, do not use.

        Use `Context.create` for command contexts.

        Use `Context.create_event_context` for extension event contexts.
        """
        self.message: osu_irc.Message | str = ""
        self.msg: osu_irc.Message | str = ""
        self.channel: osu_irc.Channel | str = ""
        self.username: str = ""
        self.user: Optional[pyosu.models.User] = None
        self.content: str = ""
        self.userid: int = -1
        self.bot: Optional[osu_irc.Client] = None
        self.command_name: str = ""
        self.api: pyosu.OsuApi = None

    @classmethod
    def create(cls, message: osu_irc.Message, user: pyosu.models.User, bot: osu_irc.Client, command_name: str="") -> "Context":
        ret = cls()
        ret.message: osu_irc.Message = message
        ret.msg: osu_irc.Message = message
        ret.channel: osu_irc.Channel = message.Channel
        ret.username: str = message.user_name
        ret.user: pyosu.models.User = user
        ret.content: str = message.content
        ret.userid: int = user.user_id
        ret.bot: osu_irc.Client = bot
        ret.command_name: str = command_name
        ret.api: pyosu.OsuApi = bot.api
        return ret

    @classmethod
    def create_event_context(cls, bot: osu_irc.Client, message: osu_irc.Message=None, user: pyosu.models.User=None) -> "Context":
        ret = cls()
        ret.bot = bot
        ret.message = message
        if message is not None:
            ret.channel = message.Channel
            ret.username = message.user_name
            ret.content = message.content
        ret.user = user
        if user is not None:
            ret.userid = user.user_id
        ret.command_name = None
        ret.api = bot.api
        return ret

    async def send(self, message: str) -> None:
        if self.channel:
            if self.channel.name.startswith("mp_"):
                await self.bot.send(message, channel=self.channel.name)
                return
        await self.bot.send(message, user=self.username)

class Command:
    # default values
    name = None
    func = None
    help = None
    admin = False
    aliases: List[str] = []

    @staticmethod
    def create_command(cls, name: str, func: Callable, help: Optional[str] = None, aliases: List[str] = []):
        """
        Creates a command object dynamically. This should not be used under normal circumstances.
        """
        cmd = cls()
        cmd.name = name
        cmd.func = func
        cmd.help = help
        cmd.aliases = aliases
        return cmd

    async def setup(self, ctx: Context):
        pass

    def shared_instance(self) -> Self:
        return command_manager.get_command(self.name)

    def __call__(self, context, *args, **kwargs) -> Any:
        return self.func(context, *args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.func}, {self.help})"

    def __str__(self):
        return repr(self)

class CommandManager:
    def __init__(self, prefix="!", bot=None) -> None:
        self.bot = bot
        self.prefix: str = prefix
        self.commands: Dict[str, Command] = {}

    async def init_manager(self, bot):
        self.bot = bot
        await self.register_all_commands()

    def register(self, command: Type[Command]) -> Command:
        cmd = command()
        logger.debug(f"Registering command {cmd.name}")
        self.commands[cmd.name] = cmd # initalize class
        return cmd

    def unregister(self, command) -> None:
        logger.debug(f"Unregistering command {command.name}")
        del self.commands[command.name]

    def get_all(self) -> Any:
        return self.commands.values()

    def get_all_names(self) -> Any:
        return self.commands.keys()

    def get_all_aliases(self) -> List[str]:
        aliases = []
        for command in self.commands.values():
            aliases += command.aliases
        return aliases

    def get_all_names_and_aliases(self) -> List[str]:
        return [*self.get_all_names(), *self.get_all_aliases()]

    def get_command(self, name) -> Optional[Command]:
        if name in self.commands:
            return self.commands[name]
        for command in self.commands.values():
            if name in command.aliases:
                return command
        return None

    def get_all_non_admin(self) -> List[Command]:
        return [command for command in self.commands.values() if not command.admin]

    async def process_message(self, message: osu_irc.Message, user) -> None:
        if message.content.startswith(self.prefix):
            command_name = message.content.split(" ")[0][1:]
            args = message.content.split(" ")[1:]
            command = self.get_command(command_name)

            if command:
                if command.admin and not user.username in [self.bot.username, "spookybear"]:
                    await self.bot.send("You do not have permission to use this command.", user=message.user_name)
                    return

                params = list(inspect.signature(command.func).parameters.values())[1:]

                for arg, param in zip(args, params):
                    try:
                        args[args.index(arg)] = param.annotation(arg)
                    except Exception:
                        pass

                context = Context.create(message, user, self.bot, command_name)
                try:
                    await command(context, *args)
                except TypeError as e:
                    if ".func() takes from" in str(e) or "required positional argument" in str(e):
                        await context.send(f"Invalid arguments for command `{command_name}`, use `{self.prefix}help {command_name}` for more info.")
                    else:
                        raise e
            else:
                raise CommandNotFound(f"Command {command_name} not found!")

    async def register_all_commands(self):
        import commands
        for command in dir(commands):
            if not command.startswith("_"):
                cmd_class = getattr(commands, command)
                if type(cmd_class) == type and Command in cmd_class.__bases__:
                    cmd = self.register(cmd_class)
                    await cmd.setup(Context.create_event_context(self.bot))
        logger.info("All commands registered")

command_manager = CommandManager()