import logging
import coloredlogs

__all__ = ["logger"]

logger = logging.getLogger("ogmios")
coloredlogs.install(level="INFO")
