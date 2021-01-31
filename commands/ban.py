from helpers.db import ban_user

async def ban(ctx, args):
    reason = args[1]
    if ctx.username == "spookybear0":
        await ban_user(ctx.username, ctx.user_id, reason)
        return "User banned!"
    else:
        return "Invalid Permissions"