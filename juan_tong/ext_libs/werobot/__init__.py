
__all__ = ["WeRoBot"]

from werobot.robot import WeRoBot
try:
    from werobot.robot import WeRoBot
except ImportError:
    pass
