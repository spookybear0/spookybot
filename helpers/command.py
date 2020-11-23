import commands

prefix = "!"

def parse_commands(args: list):
    if args[0].startswith(prefix):
        args.insert(0, args[0].replace(prefix, ""))
        args.pop(1)
        for name, handler in commands.items():
            if args[0].startswith(name):
                #try:
                msg = handler(args)
                #except Exception as e:
                #    print(f"Error in command {name}. Error: {e}")
                #    return f"Error in command {name}."
                if msg:
                    return msg

commands = {
    "pp": commands.pp,
    "ping": commands.ping
}