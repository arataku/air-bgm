import discord
from tools.logger import logger


class ChannelTool:
    async def __init__(self, guild: discord.Guild, category: discord.CategoryChannel, channel_name: str, is_voice: bool = True) -> None:
        self.guild = guild
        self.channel_name = channel_name
        self.is_voice = is_voice
        if is_voice:
            await category.create_voice_channel(channel_name)
        else:
            await category.create_text_channel(channel_name)
        logger(f"{self.channel_name} カテゴリを作成しました")


class CategoryTool:
    async def __init__(self, guild: discord.Guild, category_name: str) -> None:
        self.guild = guild
        self.category_name = self.solve_category_name(category_name)
        self.channel_tools: list[ChannelTool] = []
        self.category = await self.guild.create_category(self.category_name)
        logger(f"{self.category_name} カテゴリを作成しました")

    def solve_category_name(self, category_name) -> str:
        for i in range(100):
            name = category_name + str(i) if i != 0 else ""
            if name in [i.name for i in self.guild.channels]:
                continue
            return name
        raise Exception("カテゴリーの名前を解決できませんでした。")

    def add_channel(self, channel_name: str, is_voice: bool = True):
        self.channel_tools.append(ChannelTool(
            self.guild, self.category, channel_name, is_voice))
