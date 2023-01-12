from helpers.command import Command, Context
from typing import List

class Exec(Command):
    def __init__(self) -> None:
        self.name = "exec"
        self.help = "Executes a python command"
        self.admin = True
        self.aliases = ["py", "eval"]

    async def func(self, ctx: Context, *command_itr: List[str]) -> None:

        command: str = " ".join(command_itr)
        
        env = {
                "bot": ctx.bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "message": ctx.message,
                "api": ctx.api,
                "username": ctx.username,
            }
        command = command.replace("```py\n", "")
        command = command.strip("`")
        command = command.replace("\n", "\n    ")

        to_compile = f"import asyncio\nasync def func():\n    {command}\n\nout = asyncio.create_task(func())"

        try:
            exec_locals = {}
            exec(to_compile, env, exec_locals)

            out = exec_locals["out"]
            
            await out
        except Exception as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            out = exec_locals["out"]
            
            await out
            
            result = out.result()
            if result:
                result = str(result)
                if len(result) > 520:
                    await ctx.send("Message is over 520 characters, maybe want to fix that...")
                elif len(result) >= 130:
                    n = 130
                    result = [result[i:i+n] for i in range(0, len(result), n)]
                    for r in result:
                        await ctx.send(r)
                else:
                    await ctx.send(result)