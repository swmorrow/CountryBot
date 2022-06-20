import discord
import countrybot.modals as modals
import countrybot.utils.io as io
import countrybot.utils.embeds as emb

class CountryApprovalView(discord.ui.View): # I don't think it is possible to make this persistent, unfortunately..
    """A view attached to country approval messages which adds an approve and deny button to the message."""
    def __init__(self, user: discord.User, claimmodal, embed):
        super().__init__(timeout=None)
        self._claimant = user
        self._claimmodal = claimmodal
        self._embed = embed
        self.claim_msg = None # the message this view is attached to
        self.orig_msg = None # the original /claim message 

    @discord.ui.button(
        label="Approve",
        style=discord.ButtonStyle.green,
    )
    async def approve_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=emb.success_embed("Claim approved!"), ephemeral=True)

            button.label = "Approved"
            button.disabled = True
            self.children = [button]

            self._embed.color=discord.Color.green()
            await self.claim_msg.edit(f"<@{interaction.user.id}> has approved this claim!", view=self, embed=self._embed)

            await self.orig_msg.channel.send(
                f"<@{self._claimant.id}>",
                embed=emb.success_embed(f"{self._claimant.display_name}, your claim `{self._embed.title}` has been approved by <@{interaction.user.id}>!",
                title="Claim Approved")
            )
            self.stop()

            io.register_country()

        else:
            await interaction.response.send_message(embed=emb.error_embed("You do not have permission to approve claims!"), ephemeral=True)

    @discord.ui.button(
        label="Deny",
        style=discord.ButtonStyle.red,
    )
    async def deny_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            
            modal = modals.DenialReasonModal(title="Reason for claim denial")
            await interaction.response.send_modal(modal)
            await modal.wait()

            button.label = "Denied"
            button.disabled = True
            self.children = [button]

            msgs = {
                "deny_msg": f"<@{interaction.user.id}> has denied this claim",
                "deny_response": f"{self._claimant.display_name}, your claim \"{self._embed.title}\" has been denied by <@{interaction.user.id}>"
            }

            for k in msgs.keys():
                if modal.reason:
                    msgs[k] += f" for the following reason: `{modal.reason}`"
                else:
                    msgs[k] += "."

            self._embed.color=discord.Color.brand_red()
            await self.claim_msg.edit(msgs["deny_msg"], view=self, embed=self._embed)
            msg = await self.orig_msg.channel.send(f"<@{self._claimant.id}>", embed=emb.error_embed(msgs["deny_response"], title="Claim Denied"))
            self.stop()

        else:
            await interaction.response.send_message(embed=emb.error_embed("You do not have permission to deny claims!"), ephemeral=True)
    
    @discord.ui.button(
        label="Edit",
        style=discord.ButtonStyle.blurple,
    )
    async def edit_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if self._claimant.id == interaction.user.id:
            editmodal = modals.EditClaimModal(self._claimmodal.fields, self._claimmodal.entity, self._embed, title="Edit claim")
            await interaction.response.send_modal(editmodal)
            await editmodal.wait()
            self._embed = editmodal.embed
            await self.claim_msg.edit(embed=self._embed)

        else:
            await interaction.response.send_message(embed=emb.error_embed("You do not have permission to edit this claim!"), ephemeral=True)
    
    @discord.ui.button(
        label="Delete",
        style=discord.ButtonStyle.gray,

    )
    async def delete_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator or self._claimant.id == interaction.user.id:
            await interaction.response.send_message(embed=emb.success_embed("Claim removed."), ephemeral=True)
            await self.claim_msg.delete()
            if self._claimant.id != interaction.user.id:
                await self.orig_msg.channel.send(
                    f"<@{interaction.user.id}>",
                    embed=emb.msg_embed(f"{interaction.user.display_name}, your claim \"{self._embed.title}\" has been deleted by <@{interaction.user.id}>.")
                )
            self.stop()

        else:
            await interaction.response.send_message(embed=emb.error_embed(f"You do not have permission to delete this claim!"), ephemeral=True)


class CountryAddView(discord.ui.View):
    """A view which attaches a dropdown of available playable entities for users to click, sending a form to make a claim for said playable entity."""
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        placeholder="Pick which entity to play as",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Country", description="Play as a Country"),
            discord.SelectOption(label="Organization", description="Play as an Organization"),
            discord.SelectOption(label="Other claim", description="Play as another entity"),
        ],
    )
    async def select_callback(self, select: discord.SelectMenu, interaction: discord.Interaction):
        modal = modals.ClaimModal(select.values[0], title=f"Add new {select.values[0].lower()}")
        await interaction.response.send_modal(modal)