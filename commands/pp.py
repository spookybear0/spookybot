import requests
from helpers.np import pp as np

async def pp(ctx, args):
    map = args[1]
    return np(map)