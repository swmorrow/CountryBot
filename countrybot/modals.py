import discord
from discord.ui import InputText, Modal, View
from datetime import datetime
import countrybot.io as io
from countrybot.utils import embed_img_or_desc

class CountryAddModal(Modal):
    def __init__(self, _entity: str, user: discord.User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entity = _entity
        self._user = user

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
        country_name = self.children[0].value
        country_lore = self.children[1].value
        country_hos = self.children[2].value
        country_flag = self.children[3].value
        country_claim = self.children[4].value

        embed = discord.Embed(
            title=country_name,
            description=f"{self._entity} claim",
            color=discord.Color.random(),
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        embed.add_field(name="Brief Overview of Lore", value=country_lore, inline=False)

        if self._entity == "Country":
            if len(self.children[2].value) > 0:
                embed.insert_field_at(index=1, name="Head of State", value=country_hos, inline=False)

            if len(self.children[3].value) > 0:
                embed_img_or_desc(embed, embed.set_thumbnail, "Flag", country_flag)

            embed_img_or_desc(embed, embed.set_image, "Clam", country_claim)

        class CountryApprovalView(View):
            def __init__(self, timeout):
                super().__init__(timeout=timeout)
                self.approved = None
                self.reason = None

            @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, row=0)
            async def first_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if interaction.user.guild_permissions.administrator:
                    
                    self.approved = True
                    await interaction.response.send_message("Successfully approved the claim.", ephemeral=True)
                    self.stop()

                else:
                    await interaction.response.send_message(f"You do not have permission to approve claims!", ephemeral=True)

            @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, row=1)
            async def second_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if interaction.user.guild_permissions.administrator:
                    
                    modal = DenialReasonModal(title="Reason for claim denial")
                    await interaction.response.send_modal(modal)
                    await modal.wait()

                    self.approved = False
                    self.reason = modal.reason
                    self.stop()

                else:
                    await interaction.response.send_message(f"You do not have permission to deny claims!", ephemeral=True)
     
        approval_view = CountryApprovalView(timeout=None)
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
            await orig_msg.channel.send(f"<@{self._user.id}>, your claim \"{country_name}\" has been approved by {interaction.user.name}!")

            io.register_country()
            return

        deny_button.label = "Denied"
        deny_button.disabled = True
        approval_view.remove_item(approve_button)

        msgs = {
            "deny_msg": f"<@{interaction.user.id}> has denied this claim",
            "deny_response": f"<@{self._user.id}>, your claim \"{country_name}\" has been denied by {interaction.user.name}"
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
        
