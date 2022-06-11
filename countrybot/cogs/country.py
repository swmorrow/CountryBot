import discord
from discord.ui import Button
from discord import option, ApplicationContext, SelectOption, Interaction
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

    countrygroup = SlashCommandGroup("country", "Commands pertaining to countries and playable entities")

    approval_channelgroup = countrygroup.create_subgroup("approval_channel", "Commands pertaining to the country approval channel")


    ### COUNTRY COMMANDS ###

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
            async def select_callback(self, select, interaction: Interaction):
                modal = CountryAddModal(select.values[0], title="temp")
                modal.title = f"Add new {select.values[0]}"
                await interaction.response.send_modal(modal)

        view = CountryAddView()
        await ctx.respond("Select an entity below and click the button to create a new country/entity.", view=view, ephemeral=True)




    ### CHANNEL COMMANDS ###

    @approval_channelgroup.command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for countries awaiting approval to be posted")
    async def set(self, ctx: ApplicationContext, channel: discord.TextChannel) -> None:
        """Sets a channel for the approval queue"""

        io.save_approve_queue_channel(channel.id, ctx.guild_id)
        await ctx.respond(f"Successfully set country approval channel to <#{channel.id}>.")

    @approval_channelgroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Gets the channel used for approvals"""

        channel = io.load_approve_queue_channel(ctx.guild_id)
        if channel:
            await ctx.respond(f"The current approval channel is <#{channel}>.")
            return
            
        await ctx.respond("A country approval channel has not been set!")

    @approval_channelgroup.command()
    @has_permissions(administrator=True) # TODO: Raise error if there already is not one set.
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current approval queue channel"""

        if io.load_approve_queue_channel(ctx.guild_id):
            io.save_approve_queue_channel(None, ctx.guild_id)
            await ctx.respond("Successfully removed the country approval channel.")
            return

        await ctx.respond("A country approval channel has not been set!")

def setup(bot):
    bot.add_cog(Country(bot))