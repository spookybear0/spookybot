import os
import traceback

prefix = "!"
realpath = os.path.dirname(os.path.realpath(__file__))

def is_owner(func):
    async def decorator(ctx, args):
        if ctx.username == "spookybear0":
            return await func(ctx, args)
        else:
            from main import spookybot
            spookybot.sendPM(ctx.username, "Invalid permissions!")
    
    return decorator

async def parse_commands(args: list, ctx):
    if args[0].startswith(prefix):
        args.insert(0, args[0].replace(prefix, ""))
        args.pop(1)
        for name, info in commands.items():
            if args[0] == name:
                try:
                    msg = await info["handler"](ctx, args)
                except Exception as e:
                    print(f"Error in command {name}. Error: {e}")
                    return f"Error in command {name}. Report this to spookybear0."
                if msg:
                    return msg
            # not the original name or unknown command
            for alias in info["aliases"]:
                if args[0] == alias:
                    try:
                        msg = await info["handler"](ctx, args)
                    except Exception as e:
                        print(traceback.format_exc())
                        print(f"Error in command {name}. Error: {e}")
                        return f"Error in command {name}. Report this to spookybear0."
                    if msg:
                        return msg
                continue
        return "Unknown command!"            
    
commands = {}

def init_commands():
    global modules
    
    # get all commands dynamicly
    modules = [""]
    for file in os.listdir(realpath + f"/../commands/"):
        if os.path.isdir(realpath + f"/../commands/{file}"):
            modules.append(file)
        
    for module in modules:
        for file in os.listdir(realpath + f"/../commands/{module}"):
            if file.endswith(".py") and file != "__init__.py" and file != os.path.isdir(file):
                name = f.replace(".py", "")
                if m:
                    command = __import__(f"commands.{module}.{name}")
                else:
                    command = __import__(f"commands.{name}")
                
                try:
                    if m:
                        aliases = getattr(getattr(command, name), "aliases")
                    else:
                        aliases = getattr(getattr(command, name), "aliases")
                except AttributeError:
                    aliases = []
                
                if m:
                    commands[name] = {"handler": getattr(getattr(getattr(command, module), name), name), "aliases": aliases}
                else:
                    commands[name] = {"handler": getattr(getattr(command, name), name), "aliases": aliases}