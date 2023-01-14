from threading import Thread
from helpers.config import load_config, config
from helpers.logger import setup_logger, logger
from helpers.db import db_init
from client import SpookyBot
import asyncio
import logging
import osu_irc
import click
import signal

async def test(bot):
    await asyncio.sleep(3)
    username = input("Enter username >>> ")
    bot.test_user = username
    while True:
        inp = input(">>> ")
        msg = osu_irc.Message("")
        msg._content = inp
        msg._user_name = username

        await bot.onMessage(msg)

def exit_(sig, frame):
    logger.info("Exiting...")
    asyncio.run(main(log_level=logging.DEBUG))
    exit(0)

async def main(log_level: int=logging.INFO, testmode: bool=False):
    loop = asyncio.get_event_loop()

    signal.signal(signal.SIGINT, exit_)
    signal.signal(signal.SIGTERM, exit_)
    
    setup_logger(level=log_level)

    load_config()

    await db_init()

    spookybot = SpookyBot(token=config["token"], nickname=config["username"], loop=loop)

    config["bot"] = spookybot

    logger.info("Starting spookybot!")

    if testmode:
        logger.info("Test mode enabled!")
        spookybot.testmode = True
        Thread(target=asyncio.run, args=(test(spookybot),)).start()

    try:
        spookybot.username = config["username"]
        await spookybot.start()
    except Exception:
        pass
    finally:
        await spookybot.stop()

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