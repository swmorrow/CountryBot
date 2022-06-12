import discord
from discord.ui import InputText, Modal
from datetime import datetime
import countrybot.io as io
from countrybot.utils import embed_img_or_desc
import countrybot.views as views

class PlayableAddModal(Modal):
    """Modal for claiming a playable entity"""
    def __init__(self, entity: str, user: discord.User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entity = entity
        self._user = user
        fields = {
            "All": [
                InputText(
                    label="Official Name",
                    placeholder=f"{self._entity} name",
                    style=discord.InputTextStyle.short,
                    max_length=100
                ),
                InputText(
                    label="Brief Overview of Lore",
                    placeholder=f"{self._entity} lore \n\nWARNING: Clicking outside of this dialogue box will delete anything written.",
                    style=discord.InputTextStyle.long,
                    max_length=1024,
                )
            ],
            "Country": [
                InputText(
                    label="Head of State",
                    placeholder=f"{self._entity} head of state",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                    required=False
                ),
                InputText(
                    label="Flag",
                    placeholder=f"flag Description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024,
                    required=False
                ),
                InputText(
                    label="Land Claimed",
                    placeholder=f"claim Description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024
                )
            ],
            "Organization": [
                InputText(
                    label="Leader",
                    placeholder=f"{self._entity} leader",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                    required=False
                ),
                InputText(
                    label="Motivation",
                    placeholder=f"{self._entity} motivation",
                    style=discord.InputTextStyle.short,
                    max_length=1024
                ),
                InputText(
                    label="Emblem/flag",
                    placeholder=f"Flag description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024,
                    required=False
                )
            ],
            "Other claim": [
                InputText(
                    label="Entity",
                    placeholder="What your claim is",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                ),
                InputText(
                    label="Other info",
                    placeholder=f"Other info about your claim",
                    style=discord.InputTextStyle.long,
                    max_length=1024,
                    required=False
                ),
                InputText(
                    label="Image",
                    placeholder=f"Image description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024,
                    required=False
                ),
            ]
        }

        for entity, list in fields.items():
            if entity != "All" and entity != self._entity:
                continue
            for input_text in list:
                self.add_item(input_text)


    async def callback(self, interaction: discord.Interaction): # TODO: Add ability to edit claims
        # name = self.children[0]
        # lore = self.children[1]

        ## for countries:
        # head of state = self.children[2]
        # flag = self.children[3]
        # claim = self.children[4]

        ## for organizations:
        # leader = self.children[2]
        # motivation = self.children[3]
        # emblem/flag = self.children[4]

        ## for others:
        # entity = self.children[2]
        # other info = self.children[3]
        # image = self.children[4]

        if self._entity == "Other claim":
            self._entity = self.children[2]

        embed = discord.Embed(
            title=self.children[0].value,
            description=f"{self._entity} claim",
            color=discord.Color.random(),
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.add_field(name=self.children[1].label, value=self.children[1].value, inline=False)

        if len(self.children[2].value) > 0:
            embed.insert_field_at(index=1, name=self.children[2].label, value=self.children[2].value, inline=False)

        if len(self.children[3].value) > 0:
            if self._entity == "Country":
                embed_img_or_desc(embed, embed.set_thumbnail, self.children[3].label, self.children[3].value)
            else:
                embed.add_field(name=self.children[3].label, value=self.children[3].value, inline=False)

        if len(self.children[4].value) > 0:
            embed_img_or_desc(embed, embed.set_image, self.children[4].label, self.children[4].value)
     
        approval_view = views.CountryApprovalView(timeout=None)
        approval_channel_id = io.load_approve_channel(interaction.guild_id)

        approval_channel = await interaction.guild.fetch_channel(approval_channel_id)
        claim_msg = await approval_channel.send(embed=embed, view=approval_view)
        await interaction.response.send_message(f"Claim successfully added! An admin will approve you in <#{approval_channel_id}>.")

        await approval_view.wait()
        approve_button = approval_view.children[0]
        deny_button = approval_view.children[1]

        if approval_view.approved:
            approve_button.label = "Approved"
            approve_button.disabled = True
            approval_view.remove_item(deny_button)
        
            await claim_msg.edit(f"<@{interaction.user.id}> has approved this claim!", view=approval_view)
            orig_msg = await interaction.original_message()
            await orig_msg.channel.send(f"<@{self._user.id}>, your claim \"{self.children[0].value}\" has been approved by {interaction.user.name}!")

            io.register_country()
            return

        deny_button.label = "Denied"
        deny_button.disabled = True
        approval_view.remove_item(approve_button)

        msgs = {
            "deny_msg": f"<@{interaction.user.id}> has denied this claim",
            "deny_response": f"<@{self._user.id}>, your claim \"{self.children[0].value}\" has been denied by {interaction.user.name}"
        }

        for k in msgs.keys():
            if approval_view.reason:
                msgs[k] += f" for the following reason: {approval_view.reason}"
            else:
                msgs[k] += "."

        await claim_msg.edit(msgs["deny_msg"], view=approval_view)
        orig_msg = await interaction.original_message()
        await orig_msg.channel.send(msgs["deny_response"])

class DenialReasonModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reason = None
    
        self.add_item(
                InputText(
                    label="State your reason for denying the claim",
                    placeholder=f"(Optional) Denial reason",
                    style=discord.InputTextStyle.short,
                    required=False
                )
            )
        
    async def callback(self, interaction: discord.Interaction):
        self.reason = self.children[0].value
        self.stop()
        await interaction.response.send_message("Successfully denied the claim.", ephemeral=True)
        
