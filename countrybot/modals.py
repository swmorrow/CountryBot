import discord
from countrybot import io
from discord.ui import InputText, Modal
from countrybot.utils import embed_img_or_desc
from datetime import datetime

class CountryAddModal(Modal):
    def __init__(self, _entity: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entity = _entity

        # TODO: add customizability for which are required
        self.add_item(
            InputText(
                label="Official Name",
                placeholder=f"{self._entity} name",
                style=discord.InputTextStyle.short,
                max_length=100
            )
        )
        self.add_item(
            InputText(
                label="Brief Overview of Lore",
                placeholder=f"{self._entity} lore \n\nWARNING: Clicking outside of this dialogue box will delete anything written.",
                style=discord.InputTextStyle.long,
                max_length=1024,
            )
        )
        if self._entity == "Country":
            self.add_item(
                InputText(
                    label="Head of State",
                    placeholder=f"{self._entity} head of state",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                    required=False
                )
            )
            self.add_item(
                InputText(
                    label="Flag",
                    placeholder=f"Description/link to flag (ex. http://example.com/YYY.png",
                    style=discord.InputTextStyle.short,
                    max_length=1000,
                    required=False
                )
            )
            self.add_item(
                InputText(
                    label="Land Claimed",
                    placeholder=f"Description/link to claim (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1000
                )
            )


    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.children[0].value,
            description=f"{self._entity} claim",
            color=discord.Color.random(),
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="Brief Overview of Lore", value=self.children[1].value, inline=False)

        if self._entity == "Country":
            if len(self.children[2].value) > 0:
                embed.insert_field_at(index=1, name="Head of State", value=self.children[2].value, inline=False)

            if len(self.children[3].value) > 0:
                embed_img_or_desc(embed, embed.set_thumbnail, "Flag", self.children[3].value)

            embed_img_or_desc(embed, embed.set_image, "Clam", self.children[4].value)

        approval_channel = io.load_approve_queue_channel(interaction.guild_id) # TODO: add view
        if approval_channel:

            channel = await interaction.guild.fetch_channel(approval_channel)
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Country successfully added! An admin will approve you in <#{approval_channel}>")
            return

        await interaction.response.send_message(embed=embed)