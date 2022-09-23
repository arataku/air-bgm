import asyncio
import discord
from discord.ext import commands
import os
from tools.logger import logger

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=intents)
bot.application_id

COGS: list[str] = ["ping"]


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync(guild=discord.Object(836210809754746931))


async def cog_setup():
    # Cogs
    for cog in COGS:
        await bot.load_extension(f"Cogs.{cog}")
        logger(f"loaded \"{cog}\"")

if __name__ == "__main__":
    asyncio.run(cog_setup())
    bot.run(os.environ["AirBOT_TOKEN"])
