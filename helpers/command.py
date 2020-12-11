import commands

prefix = "!"

async def parse_commands(args: list, ctx: dict):
    if args[0].startswith(prefix):
        args.insert(0, args[0].replace(prefix, ""))
        args.pop(1)
        for name, handler in commands.items():
            if args[0].startswith(name):
                #try:
                msg = await handler(ctx, args)
                #except Exception as e:
                #    print(f"Error in command {name}. Error: {e}")
                #    return f"Error in command {name}."
                if msg:
                    return msg

commands = {
    "pp": commands.pp,
    "ping": commands.ping,
    "recent": commands.recent,
    "user": commands.user,
    "rank": commands.rank,
    "top": commands.top,
    "help": commands.help
}