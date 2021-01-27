from helpers.np import pp as np

async def pp(ctx, args):
    try:
        map = args[1]
    except IndexError:
        return "Invalid arguments."
    
    return await np(map)