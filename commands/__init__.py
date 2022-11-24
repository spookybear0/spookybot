try:
    from .ping import Ping
    from .user import User
    from .info import Info
    from .help import Help
    from .versus import Versus
    from .github import Github
    from .recent import Recent
    from .rank import Rank
    from .mods import Mods
    from .acc import Acc
    from .watch import Watch
    from .unwatch import Unwatch
except Exception:
    import traceback
    traceback.print_exc()