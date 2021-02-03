import os, traceback

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
    if os.name == "nt":
        divider = "\\"
    elif os.name == "posix":
        divider = "/"
    else:
        divider = "/"

    modules = [""]
    for f in os.listdir(realpath + f"{divider}..{divider}commands{divider}"):
        if os.path.isdir(realpath + f"{divider}..{divider}commands{divider}{f}"):
            modules.append(f)
            
        
    for m in modules:
        for f in os.listdir(realpath + f"{divider}..{divider}commands{divider}{m}"):
            if f.endswith(".py") and f != "__init__.py" and f != os.path.isdir(f):
                name = f.replace(".py", "")
                if m:
                    command = __import__(f"commands.{m}.{name}")
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
                    commands[name] = {"handler": getattr(getattr(getattr(command, m), name), name), "aliases": aliases}
                else:
                    commands[name] = {"handler": getattr(getattr(command, name), name), "aliases": aliases}