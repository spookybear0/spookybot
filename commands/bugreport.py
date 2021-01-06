import os

async def bugreport(ctx, args):
    bug = args[1]
    # check if it is in quotes
    if len(bug.split(" ")) < 2:
        return "Use quotes for sentences with more than one word."
    if not os.path.exists("bugreport.txt"):
        open("bugreport.txt", "w").close()
    f = open("bugreport.txt", "a")
    f.write(bug + "\n")
    f.close()
    return "Bug report submitted! Remember, if you want your bug report to go faster, create an issue on github (!github)"