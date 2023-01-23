from datetime import datetime
from helpers.config import config
import logging
import asyncio
import os

logger = logging.getLogger("spookybot")

class OsuDebugHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        if config.get("bot") is not None:
            asyncio.run_coroutine_threadsafe(config["bot"].send(f"{record.levelname} - {record.message}", user="spookybear", nodebug=True), asyncio.get_event_loop())

def setup_logger(level: int=logging.INFO) -> None:
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if not os.path.exists("logs/"):
        os.mkdir("logs/")
    file_handler = logging.FileHandler(datetime.now().strftime("logs/spookybot_%Y_%m_%d_%H_%M_%S.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)