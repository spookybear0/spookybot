from datetime import datetime
import logging
import os

logger = logging.getLogger("spookybot")

def setup_logger(level: int=logging.INFO):
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if not os.path.exists("logs/"):
        os.mkdir("logs/")
    file_handler = logging.FileHandler(datetime.now().strftime("logs/spookybot_%H_%M_%S_%d_%m_%Y.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)