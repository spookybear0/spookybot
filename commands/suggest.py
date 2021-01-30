import os
from helpers.db import add_suggestion

async def suggest(ctx, args):
    bug = args[1]
    # check if it is in quotes
    if len(bug.split(" ")) < 2:
        return "Use quotes for sentences with more than one word."
    add_suggestion(ctx.username, ctx.user_id, bug)
    return "Suggestion submitted! You can also create an issue on github to be responded to faster (!github)."

aliases = ["sg"]