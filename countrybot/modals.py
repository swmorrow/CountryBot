from typing import Dict, List
import discord
from discord.ui import InputText, Modal
import countrybot.utils.io as io
import countrybot.utils.embeds as emb
import countrybot.views as views

class ClaimModal(Modal):
    """Modal for claiming a playable entity"""
    def __init__(self, entity: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.entity = entity.removesuffix(" Claim")
        self.fields = {
            "All": [
                InputText(
                    label="Official Name",
                    placeholder=f"{self.entity} name",
                    style=discord.InputTextStyle.short,
                    max_length=100
                ),
                InputText(
                    label="Brief Overview of Lore",
                    placeholder=f"{self.entity} lore \n\nWARNING: Clicking outside of this dialogue box will delete anything written.",
                    style=discord.InputTextStyle.long,
                    max_length=4000
                )
            ],
            "Country": [
                InputText(
                    label="Head of State",
                    placeholder=f"{self.entity} head of state",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                    required=False
                ),
                InputText(
                    label="Flag",
                    placeholder=f"Flag description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024,
                    required=False
                ),
                InputText(
                    label="Claimed Land",
                    placeholder=f"Claim description/link (ex. http://example.com/YYY.png)",
                    style=discord.InputTextStyle.short,
                    max_length=1024
                )
            ],
            "Organization": [
                InputText(
                    label="Leader",
                    placeholder=f"{self.entity} leader",
                    style=discord.InputTextStyle.short,
                    max_length=100,
                    required=False
                ),
                InputText(
                    label="Motivation",
                    placeholder=f"{self.entity} motivation",
                    style=discord.InputTextStyle.short,
                    max_length=1024
                ),
                InputText(
                    label="Emblem/Flag",
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

        for entity, list in self.fields.items():
            if entity != "All" and entity != self.entity:
                continue
            for input_text in list:
                self.add_item(input_text)


    async def callback(self, interaction: discord.Interaction):
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

        embed = await emb.children_to_embed(self.children, self.entity, interaction.user)
        approval_channel_id = io.load_approve_channel(interaction.guild_id)
        approval_channel = await interaction.guild.fetch_channel(approval_channel_id)    
        approval_view = views.CountryApprovalView(interaction.user, self, embed)
        approval_view.claim_msg = await approval_channel.send(embed=embed, view=approval_view)

        await interaction.response.send_message(embed=emb.success_embed(f"Claim added! An admin will approve you in <#{approval_channel_id}>."), ephemeral=True)
        
        orig_msg = await interaction.original_response()
        approval_view.orig_msg = orig_msg

        await approval_view.wait()

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
        await interaction.response.send_message(embed=emb.success_embed("Claim denied"), ephemeral=True)

class EditClaimModal(Modal):
    def __init__(self, fields: Dict[str,List[InputText]], entity: str, embed: discord.Embed, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._fields = fields
        self._entity = entity
        self.embed = embed

        for entity, list in self._fields.items(): # Populates the modal fields with the embed info
            if entity != "All" and entity != self._entity:
                continue

            for input_text in list:
                if input_text.label == "Official Name":
                    input_text.value = embed.title

                if input_text.label == "Brief Overview of Lore":
                    input_text.value = embed.description

                if input_text.label in ["Image", "Emblem/Flag", "Claimed Land"] and embed.image:
                    input_text.value = embed.image.url
            
                if input_text.label == "Flag" and embed.thumbnail:
                    input_text.value = embed.thumbnail.url

                for field in embed.fields:
                    name = field.name.removesuffix(" Description")
                    name = name.removesuffix(" Link")
                    if name != input_text.label:
                        continue

                    input_text.value = field.value
                    break

                self.add_item(input_text)
                
    async def callback(self, interaction: discord.Interaction):
        self.embed = await emb.children_to_embed(self.children, self._entity, interaction.user, self.embed)
        await interaction.response.send_message(embed=emb.success_embed("Claim edited!"), ephemeral=True)
        self.stop()
