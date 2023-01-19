try:
    from .np import NPExtension
    from .matchmaker import Matchmaker
    from .banchobot import BanchoBot
    from .watch import Watch
    from .discordbot import Discord
    from .recommend import Recommend
except Exception:
    import traceback
    traceback.print_exc()