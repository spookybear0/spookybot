from helpers.command import Command, Context, command_manager
from typing import List, Optional, Union, _UnionGenericAlias
from helpers.models import Hidden
import inspect
import math

class Help(Command):
    def __init__(self) -> None:
        self.name = "help"
        self.help = "Shows this message."

    async def func(self, ctx: Context, command: Optional[Union[str, int]]=None) -> None:
        try:
            pagenum: Optional[int] = int(command)
        except (ValueError, TypeError):
            pagenum: Optional[int] = None
        
        if command is None or pagenum is not None:
            if pagenum is None:
                pagenum = 1

            pages_available: int = math.ceil(len(command_manager.get_all_non_admin())/3)

            if pagenum > pages_available:
                return await ctx.send(await ctx.bot.lang.get(ctx, "page_not_found", pagenum, pages_available))

            cmds: List[Command] = list(command_manager.get_all_non_admin())[(pagenum*3)-3:(pagenum*3)]

            cmd_list: List[str] = [await ctx.bot.lang.get(ctx, "pages_available", pagenum, pages_available)]

            for i, cmd in enumerate(cmds, 1):
                params_ = list(inspect.signature(cmd.func).parameters.values())[1:]
                params: List[str] = []

                for param in params_:
                    hide = False
                    paramstring = str(param)

                    if type(param.annotation) is _UnionGenericAlias:
                        hint = ""
                        for j, annotation in enumerate(param.annotation.__args__):
                            if annotation is not type(None):
                                if j != 0:
                                    hint += "|"
                                hint += annotation.__name__

                        paramstring = f"{param.name}: {hint}"

                    if param.annotation is Hidden:
                        hide = True
                                
                    if not hide:
                        if param.default is param.empty:
                            # required
                            params.append(f'<{str(paramstring).replace(" ", "").replace(":", ": ")}>')
                        else:
                            # not required
                            params.append(f'[{str(paramstring).replace(" ", "").replace(":", ": ")}]')

                cmd_list.append(f"{(pagenum*3)-3+i}. - {command_manager.prefix}{cmd.name}{' ' if params else ''}{' '.join(params)}: {cmd.help}")

            for cmd in cmd_list:
                await ctx.send(cmd)
            return await ctx.send(await ctx.bot.lang.get(ctx, "help_info"))
        else:
            command = command_manager.get_command(command)

            if command is None:
                return await ctx.send(await ctx.bot.lang.get(ctx, "command_not_found"))

            await ctx.send(f"{command.name}: {command.help}")
            await ctx.send(f"Aliases: {', '.join(command.aliases)}")