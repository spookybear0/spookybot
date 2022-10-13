from tortoise import Tortoise
from helpers.config import config
from helpers.logger import logger

async def db_init():
    logger.info("Initalizing database")

    await Tortoise.init(
        db_url=f"sqlite://{config['sqlite_file']}",
        modules={"models": ["helpers.models"]}
    )
    #await Tortoise.generate_schemas() # create tables