from dis import dis
from pyclbr import Function
from typing import Any, Callable
from venv import create
import discord

from tools.logger import logger


class CreateView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)

    def add_button(self, style: discord.ButtonStyle = ..., label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None, on_click: Callable | None = None, change_disabled: bool = True):
        self.add_item(CreateButton(style=style, label=label, disabled=disabled,
                      custom_id=custom_id, emoji=emoji, on_click=on_click, create_view=self, change_disabled=change_disabled))


class CreateButton(discord.ui.Button):
    def __init__(self, *, style: discord.ButtonStyle = ..., label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None, on_click: Callable | None = None, create_view: CreateView | None = None, change_disabled: bool = True):
        super().__init__(style=style, label=label, disabled=disabled,
                         custom_id=custom_id, emoji=emoji, row=row)
        self.on_click = on_click
        self.create_view = create_view
        self.change_disabled = change_disabled

    async def callback(self, interaction: discord.Interaction) -> Any:
        logger("callback")
        if self.create_view is not None and self.change_disabled:
            self.disabled = True
            await interaction.response.edit_message(view=self.create_view)
        if self.on_click is not None:
            await self.on_click(interaction)
        return await super().callback(interaction)


class MsgTool:
    def __init__(self) -> None:
        self.content = None
        self.embed = None
        self.view: CreateView = CreateView()

    def set_content(self, content: str | None) -> "MsgTool":
        self.content = content
        return self

    def set_embed(self, title: Any | None = None, description: Any | None = None, color: int | discord.Colour | None = None) -> "MsgTool":
        self.embed = discord.Embed(
            title=title, description=description, color=color)
        return self

    def embed_change_option(self,  title: Any | None = None, description: Any | None = None):
        if self.embed is None:
            return
        if title is not None:
            self.embed.title = title
        if description is not None:
            self.embed.description = description

    def embed_add_field(self, name: Any, value: Any, inline: bool = True) -> "MsgTool":
        if self.embed is None:
            print("先にset_embedでembedを設定してください。")
        else:
            self.embed.add_field(name=name, value=value, inline=inline)
        return self

    def add_button(self, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None, on_click: Callable[[discord.Interaction], Any] | None = None, change_disabled: bool = True):
        self.view.add_button(style=style, label=label,
                             disabled=disabled, custom_id=custom_id, emoji=emoji, row=row, on_click=on_click, change_disabled=change_disabled)
        return self

    def remove_button(self):
        self.view.clear_items()

    def copy(self):
        tmp = MsgTool()
        tmp.content = self.content
        tmp.embed = self.embed
        return tmp

    def create(self) -> dict:
        return {"content": self.content, "embed": self.embed, "view": self.view}
