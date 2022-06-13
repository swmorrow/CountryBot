from typing import Dict, List
import discord
from discord.ui import InputText, Modal
from datetime import datetime
import countrybot.io as io
from countrybot.utils import children_to_embed, embed_img_or_desc
import countrybot.views as views

class PlayableAddModal(Modal):
    """Modal for claiming a playable entity"""
    def __init__(self, entity: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entity = entity
        self._fields = {
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

        for entity, list in self._fields.items():
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

        embed = children_to_embed(self.children, self._entity, interaction.user)
     
        approval_view = views.CountryApprovalView(interaction.user, timeout=None)
        approval_channel_id = io.load_approve_channel(interaction.guild_id)

        approval_channel = await interaction.guild.fetch_channel(approval_channel_id)
        claim_msg = await approval_channel.send(embed=embed, view=approval_view)
        await interaction.response.send_message(f"Claim successfully added! An admin will approve you in <#{approval_channel_id}>.", ephemeral=True)

        await approval_view.wait()

        approve_button = approval_view.children[0]
        deny_button = approval_view.children[1]
        edit_button = approval_view.children[2]
        delete_button = approval_view.children[3]
        orig_msg = await interaction.original_message()

        if approval_view.deleter:
            await claim_msg.delete()
            if interaction.user.id != approval_view.deleter.id:
                await orig_msg.channel.send(f"<@{interaction.user.id}>, your claim \"{self.children[0].value}\" has been deleted by {approval_view.deleter.name}.")

        elif approval_view.edit_interaction:
            modal = EditClaimModal(self._fields, self._entity, embed, title="Edit your claim")
            await approval_view.edit_interaction.response.send_modal(modal)
            await modal.wait()
            await claim_msg.edit(view=views.CountryApprovalView(interaction.user, timeout=None), embed=modal.embed)

        elif approval_view.approved:
            approve_button.label = "Approved"
            approve_button.disabled = True
            approval_view.remove_item(deny_button)
            approval_view.remove_item(delete_button)
            approval_view.remove_item(edit_button)

            embed.color=discord.Color.green()
            await claim_msg.edit(f"<@{approval_view.approver.id}> has approved this claim!", view=approval_view, embed=embed)
            await orig_msg.channel.send(f"<@{interaction.user.id}>, your claim \"{self.children[0].value}\" has been approved by {approval_view.approver.name}!")

            io.register_country()
            return
        
        else:
            deny_button.label = "Denied"
            deny_button.disabled = True
            approval_view.remove_item(approve_button)
            approval_view.remove_item(delete_button)
            approval_view.remove_item(edit_button)

            msgs = {
                "deny_msg": f"<@{approval_view.approver.id}> has denied this claim",
                "deny_response": f"<@{interaction.user.id}>, your claim \"{self.children[0].value}\" has been denied by {approval_view.approver.name}"
            }

            for k in msgs.keys():
                if approval_view.reason:
                    msgs[k] += f" for the following reason: {approval_view.reason}"
                else:
                    msgs[k] += "."

            embed.color=discord.Color.brand_red()
            await claim_msg.edit(msgs["deny_msg"], view=approval_view, embed=embed)
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

class EditClaimModal(Modal):
    def __init__(self, fields: Dict[str,List[InputText]], entity: str, embed: discord.Embed, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._fields = fields
        self._entity = entity
        self.embed = embed

        for entity, list in self._fields.items():
            if entity != "All" and entity != self._entity:
                continue
            for input_text in list:
                for field in embed.fields:
                    if field.name.removesuffix(" Description") != input_text.label:
                        continue
                    input_text.value = field.value
                    break

                self.add_item(input_text)
                
    async def callback(self, interaction: discord.Interaction):
        self.embed = children_to_embed(self.children, self._entity, interaction.user)
        await interaction.response.send_message("Successfully edited claim!", ephemeral=True)
        self.stop()
