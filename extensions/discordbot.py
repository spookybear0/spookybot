import discord
from typing import Optional, List
from helpers.extension import Extension
from helpers.command import Context
from helpers.config import config
from helpers.logger import logger
import osu_irc

bot = discord.Bot()

class Discord(Extension):
    def __init__(self) -> None:
        self.name = "discord"
        self.help = "Discord bot interaction extension."
        self.irc_bot: Optional[osu_irc.Client] = None
        self.bot: discord.Bot = bot

    async def setup(self, ctx: Context) -> None:
        self.irc_bot = ctx.bot

        logger.debug("Starting discord bot thread")

        self.start_async_thread(self.discord_thread)

    async def discord_thread(self) -> None:
        logger.info("Starting discord bot")

        await self.bot.start(config["discordbottoken"])

irc_bot = Discord().shared_instance

@bot.event
async def on_ready() -> None:
    logger.info("Discord bot is ready")

@bot.slash_command(guild_ids=[config["discordguildid"]], description="Pings discord and returns the latency.")
async def ping(ctx) -> None:
    await ctx.respond(f"Pong {bot.latency*1000:.2f}ms")