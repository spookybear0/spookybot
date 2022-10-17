from threading import Thread
from helpers.config import load_config, config
from helpers.logger import setup_logger, logger
from helpers.db import db_init
from client import SpookyBot
import asyncio
import logging
import osu_irc
import click

nickname = "spookybear0"

async def test(bot):
    await asyncio.sleep(3)
    username = input("Enter username >>> ")
    while True:
        inp = input(">>> ")
        msg = osu_irc.Message("")
        msg._content = inp
        msg._user_name = username

        await bot.onMessage(msg)

async def main(log_level: int=logging.INFO, testmode: bool=False):
    loop = asyncio.get_event_loop()
    
    setup_logger(level=log_level)

    load_config()

    await db_init()

    spookybot = SpookyBot(token=config["token"], nickname=nickname, loop=loop)

    logger.info("Starting spookybot!")

    if testmode:
        logger.info("Test mode enabled!")
        spookybot.testmode = True
        Thread(target=asyncio.run, args=(test(spookybot),)).start()

    await spookybot.start()

@click.command()
@click.option("--debug", is_flag=True, help="Enables debug mode")
@click.option("--testmode", is_flag=True, help="Enables test mode")
def cli(debug, testmode):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    asyncio.run(main(log_level=level, testmode=testmode))

if __name__ == "__main__":
    cli()