import os

prefix = "!"
realpath = os.path.dirname(os.path.realpath(__file__))

async def parse_commands(args: list, ctx: dict):
    if args[0].startswith(prefix):
        args.insert(0, args[0].replace(prefix, ""))
        args.pop(1)
        for name, handler in commands.items():
            if args[0].startswith(name):
                try:
                    msg = await handler(ctx, args)
                except Exception as e:
                    print(f"Error in command {name}. Error: {e}")
                    return f"Error in command {name}. Report this to spookybear0."
                if msg:
                    return msg

commands = {}

# get all commands dynamicly
for f in os.listdir(realpath + "\\..\\commands"): # commands folder
    if f.endswith(".py") and f != "__init__.py" and f != os.path.isdir(f):
        name = f.replace(".py", "")
        commands[name] = getattr(__import__(f"commands.{name}"), name)