import discord
import countrybot.modals as modals

class CountryApprovalView(discord.ui.View):
    """A view attached to country approval messages which adds an approve and deny button to the message."""
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.approved = None
        self.reason = None

    @discord.ui.button(label="Approve", custom_id="approve_button", style=discord.ButtonStyle.green)
    async def first_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            
            self.approved = True
            await interaction.response.send_message("Successfully approved the claim.", ephemeral=True)
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to approve claims!", ephemeral=True)

    @discord.ui.button(label="Deny", custom_id="deny_button", style=discord.ButtonStyle.red)
    async def second_button_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            
            modal = modals.DenialReasonModal(title="Reason for claim denial")
            await interaction.response.send_modal(modal)
            await modal.wait()

            self.approved = False
            self.reason = modal.reason
            self.stop()

        else:
            await interaction.response.send_message(f"You do not have permission to deny claims!", ephemeral=True)

class CountryAddView(discord.ui.View):
    """A view which attaches a dropdown of available playable entities for users to click, sending a form to make a claim for said playable entity."""
    def __init__(self, user: discord.User):
        super().__init__()
        self._user = user

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
        modal = modals.PlayableAddModal(select.values[0], self._user, title=f"Add new {select.values[0]}")
        await interaction.response.send_modal(modal)