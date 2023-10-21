import os
import logging
import coloredlogs

__all__ = ["logger"]

logger = logging.getLogger("ogmios")
os.environ["COLOREDLOGS_LOG_FORMAT"] = '%(asctime)s - %(levelname)s - %(message)s'
coloredlogs.install(level="INFO")
