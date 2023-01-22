try:
    from .ping import Ping
    from .user import User
    from .info import Info
    from .help import Help
    from .versus import Versus
    from .recent import Recent
    from .rank import Rank
    from .mods import Mods
    from .acc import Acc
    from .watch import Watch
    from .unwatch import Unwatch
    from .recommend import Recommend
    from .language import Language

    # admin commands
    from .admin.create_match import CreateMatch
    from .admin.close_match import CloseMatch
    from .admin.msg import Message
    from .admin.close_all_matches import CloseAllMatches
    from .admin.exec import Exec
    from .admin.debug import Debug
    from .admin.add_user import AddUser
except Exception:
    import traceback
    traceback.print_exc()