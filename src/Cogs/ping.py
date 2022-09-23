import discord
from discord import app_commands
from discord.ext import commands


class ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command()
    @app_commands.guilds(703129045201846372, 836210809754746931, 727823966303158293)
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong!")


async def setup(bot: commands.Bot):
    await bot.add_cog(ping(bot))
