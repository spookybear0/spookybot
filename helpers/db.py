from tortoise import Tortoise
from helpers.config import config

async def db_init():
    await Tortoise.init(
        db_url=f"sqlite://{config['sqlite_file']}",
        modules={"models": ["helpers.models"]}
    )
    #await Tortoise.generate_schemas() # create tables