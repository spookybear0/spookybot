from tortoise import Tortoise
from helpers.config import config
from helpers.logger import logger

tortoise_config = {
    "connections": {"default": f"sqlite://{config['sqlite_file']}"},
    "apps": {
        "models": {
            "models": ["helpers.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}

async def db_init() -> None:
    logger.info("Initalizing database")

    await Tortoise.init(
        config=tortoise_config
    )
    #await Tortoise.generate_schemas() # create tables