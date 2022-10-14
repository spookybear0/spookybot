from ctypes import Union
from typing import Dict, Optional, Callable, List, Type, TYPE_CHECKING
from collections.abc import KeysView, ValuesView
from helpers.exceptions import CommandNotFound
from helpers.logger import logger
import inspect
import osu_irc
import pyosu

class Context:
    def __init__(self, message: osu_irc.Message=None, user: pyosu.models.User=None, bot: osu_irc.Client=None, command_name: str="", lazy_init=False) -> None:
        if lazy_init:
            return
        self.message: osu_irc.Message = message
        self.msg: osu_irc.Message = message
        self.username: str = message.user_name
        self.user: pyosu.models.User = user
        self.content: str = message.content
        self.userid: int = user.user_id
        self.bot: osu_irc.Client = bot
        self.command_name: str = command_name

    @classmethod
    def create_event_context(cls, bot: osu_irc.Client, message: osu_irc.Message=None, user: pyosu.models.User=None) -> None:
        ret = cls(lazy_init=True)
        ret.bot = bot
        ret.message = message
        if message is not None:
            ret.username = message.user_name
            ret.content = message.content
        ret.user = user
        if user is not None:
            ret.userid = user.user_id
        ret.command_name = None
        return ret

    async def send(self, message: str) -> None:
        await self.bot.send(message, user=self.username)

class Command:
    # default values
    name = None
    func = None
    help = None
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

    def __call__(self, context, *args, **kwargs):
        return self.func(context, *args, **kwargs)

    def __repr__(self):
        return f"Command({self.name}, {self.func}, {self.help})"

    def __str__(self):
        return self.name

class CommandManager:
    def __init__(self, prefix="!", bot=None) -> None:
        self.bot = bot
        self.prefix: str = prefix
        self.commands: Dict[str, Command] = {}

    def init_manager(self, bot):
        self.bot = bot
        self.register_all_commands()

    def register(self, command: Type[Command]) -> None:
        cmd = command()
        logger.debug(f"Registering command {cmd.name}")
        self.commands[cmd.name] = cmd # initalize class

    def unregister(self, command) -> None:
        logger.debug(f"Unregistering command {command.name}")
        del self.commands[command.name]

    def get_all(self) -> ValuesView[Command]:
        return self.commands.values()

    def get_all_names(self) -> KeysView[str]:
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

    async def process_message(self, message: osu_irc.Message, user):
        if message.content.startswith(self.prefix):
            command_name = message.content.split(" ")[0][1:]
            args = message.content.split(" ")[1:]
            command = self.get_command(command_name)

            if command:
                params = list(inspect.signature(command.func).parameters.values())[1:]

                for arg, param in zip(args, params):
                    try:
                        args[args.index(arg)] = param.annotation(arg)
                    except Exception:
                        pass

                context = Context(message, user, self.bot, command_name)
                await command(context, *args)
            else:
                raise CommandNotFound(f"Command {command_name} not found!")

    def register_all_commands(self):
        import commands
        for command in dir(commands):
            if not command.startswith("_"):
                cmd_class = getattr(commands, command)
                if type(cmd_class) == type and Command in cmd_class.__bases__:
                    self.register(cmd_class)
        logger.info("All commands registered")

command_manager = CommandManager()