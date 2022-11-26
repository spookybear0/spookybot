try:
    from .np import NPExtension
    from .matchmaker import Matchmaker
    from .banchobot import BanchoBot
    from .watch import Watch
    from .discord_bot import Discord
except Exception:
    import traceback
    traceback.print_exc()