import discord
from discord import SelectOption
from discord.ext import commands
from discord.ui import InputText, Modal, Select

class CountryAddModal(Modal):
    def __init__(self, entity: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Name", placeholder=f"{entity} Name"))

        self.add_item(
            InputText(
                label="Lore",
                placeholder=f"{entity} Lore",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Modal")
        return
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])