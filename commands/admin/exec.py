from helpers.command import Command, Context
from typing import List

class Exec(Command):
    def __init__(self) -> None:
        self.name = "exec"
        self.help = "Executes a python command"
        self.admin = True
        self.aliases = ["py", "eval"]

    async def func(self, ctx: Context, *command_itr: List[str]) -> None:
        return
        command: str = " ".join(command_itr)
        
        exec(command)