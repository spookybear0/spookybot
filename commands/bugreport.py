import os
from helpers.db import report_bug

async def bugreport(ctx, args):
    bug = args[1]
    # check if it is in quotes
    if len(bug.split(" ")) < 2:
        return "Use quotes for sentences with more than one word."
    report_bug(ctx.username, ctx.user_id, bug)
    return "Bug report submitted! Remember, if you want your bug report to go faster, create an issue on github (!github)"

aliases = ["br"]