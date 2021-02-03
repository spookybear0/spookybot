from helpers.db import ban_user
from helpers.command import is_owner

@is_owner
async def ban(ctx, args):
    reason = args[1]
    await ban_user(ctx.username, ctx.user_id, reason)
    return "User banned!"