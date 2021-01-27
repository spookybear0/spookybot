import os

async def suggest(ctx, args):
    bug = args[1]
    # check if it is in quotes
    if len(bug.split(" ")) < 2:
        return "Use quotes for sentences with more than one word."
    if not os.path.exists("suggest.txt"):
        open("suggest.txt", "w").close()
    f = open("suggest.txt", "a")
    f.write(bug + "\n")
    f.close()
    return "Suggestion submitted! You can also create an issue on github to be responded to faster (!github)."

aliases = ["sg"]