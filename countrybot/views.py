import discord
import countrybot.modals as modals

class CountryApprovalView(discord.ui.View):
    """A view attached to country approval messages which adds an approve and deny button to the message."""
    def __init__(self, user: discord.User, timeout):
        super().__init__(timeout=timeout)
        self._user = user
        self.approver = None
        self.reason = None
        self.deleter = None
        self.edit_interaction = None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def first_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            
            self.approved = True
            self.approver = interaction.user
            await interaction.response.send_message("Successfully approved the claim.", ephemeral=True)
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to approve claims!", ephemeral=True)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def second_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            
            modal = modals.DenialReasonModal(title="Reason for claim denial")
            await interaction.response.send_modal(modal)
            await modal.wait()

            self.approved = False
            self.approver = interaction.user
            self.reason = modal.reason
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to deny claims!", ephemeral=True)
    
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple)
    async def third_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if self._user.id == interaction.user.id:
            self.edit_interaction = interaction
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to edit this claim!", ephemeral=True)
    
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.gray)
    async def fourth_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator or self._user.id == interaction.user.id:
            await interaction.response.send_message("Successfully removed claim.", ephemeral=True)
            self.deleter = interaction.user
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to delete this claim!", ephemeral=True)

    # TODO
    # @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray)
    # async def third_button_callback(self, button: discord.Button, interaction: discord.Interaction):
    #     if interaction.user == self._user:
            
    #         modal = modals.PlayableAddModal(embed., title="Edit claim")
    #         for field in self._embed.fields:

    #         await interaction.response.send_modal(modal)
    #         await modal.wait()

    #         self.approved = False
    #         self.approver = interaction.user
    #         self.reason = modal.reason
    #         self.stop()

    #     else:
    #         await interaction.response.send_message(f"You do not have permission to edit this claim!", ephemeral=True)

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
        modal = modals.PlayableAddModal(select.values[0], title=f"Add new {select.values[0]}")
        await interaction.response.send_modal(modal)