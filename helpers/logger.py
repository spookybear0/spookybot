import logging

logger = logging.getLogger("spookybot")

def setup_logger(level: int=logging.INFO):
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(name)s - %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)