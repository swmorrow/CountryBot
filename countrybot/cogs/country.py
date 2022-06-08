import discord
from discord.ui import Button
from discord import option, ApplicationContext, SelectOption
from countrybot import io
from countrybot.rpdate import RPDate
from countrybot.modals import CountryAddModal
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions


class Country(commands.Cog):
    r"""A collection of the commands pertaining to countries.

    Attributes
    ------------
    bot: :class:`discord.Bot`
        The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot

    countrygroup = SlashCommandGroup("country", "Commands pertaining to the RP date")
    
    ### COMMANDS ###

    @countrygroup.command() # TODO: Add support for other entities (orgs, characters, etc)
    async def add(self, ctx: ApplicationContext): # maybe make an option for the message to not be ephemeral?
        """Send a modal to the user to add a country/entity"""

        class CountryAddView(discord.ui.View):
            @discord.ui.select(
                placeholder="Pick which entity to play as",
                min_values=1,
                max_values=1,
                options=[
                    SelectOption(label="Country", description="Play as a Country"),
                    SelectOption(label="Organization", description="Play as an Organization"),
                    SelectOption(label="Character", description="Play as a Character"),
                ],
            )
            async def select_callback(self, select, interaction):
                modal = CountryAddModal(select.values[0], title="temp")
                modal.title = f"Add new {select.values[0]}"
                await interaction.response.send_modal(modal)

        view = CountryAddView()
        await ctx.respond("Select an entity below and click the button to create a new country/entity", view=view, ephemeral=True)



def setup(bot):
    bot.add_cog(Country(bot))