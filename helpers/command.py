import os

prefix = "!"
realpath = os.path.dirname(os.path.realpath(__file__))

async def parse_commands(args: list, ctx: dict):
    if args[0].startswith(prefix):
        args.insert(0, args[0].replace(prefix, ""))
        args.pop(1)
        for name, info in commands.items():
            if args[0].startswith(name):
                try:
                    msg = await info["handler"](ctx, args)
                except Exception as e:
                    print(f"Error in command {name}. Error: {e}")
                    return f"Error in command {name}. Report this to spookybear0."
                if msg:
                    return msg
            else: # not the original name or unknown command
                for alias in info["aliases"]:
                    if args[0].startswith(alias):
                        try:
                            msg = await info["handler"](ctx, args)
                        except Exception as e:
                            print(f"Error in command {name}. Error: {e}")
                            return f"Error in command {name}. Report this to spookybear0."
                        if msg:
                            return msg
                # no commands matched
                return "Unknown command, type !help to get a list of commands!"
                

commands = {}

# get all commands dynamicly
if os.name == "nt":
    divider = "\\"
elif os.name == "posix":
    divider = "/"
else:
    divider = "/"

for f in os.listdir(realpath + f"{divider}..{divider}commands"): # commands folder
        if f.endswith(".py") and f != "__init__.py" and f != os.path.isdir(f):
            name = f.replace(".py", "")
            command = __import__(f"commands.{name}")
            
            try:
                aliases = getattr(getattr(command, "recommend"), "aliases")
            except AttributeError:
                aliases = []
            
            commands[name] = {"handler": getattr(command, name), "aliases": aliases}