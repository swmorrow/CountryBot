import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup, slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions

import countrybot.io as io
import countrybot.views as views

class Playable(commands.Cog):
    r"""A collection of the commands pertaining to playables.

    Attributes
    ------------
    bot: :class:`discord.Bot`
        The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot: discord.bot):
        self.bot = bot

    countrygroup = SlashCommandGroup("country", "Commands pertaining to countries")
    # orggroup = SlashCommandGroup("organizaiton", "Commands pertaining to organizations") # To be implemented
    # chargroup = SlashCommandGroup("character", "Commands pertaining to characters") # To be implemented
    approval_channelgroup = SlashCommandGroup("approval_channel", "Commands pertaining to the country approval channel")

    @slash_command() # TODO: Add support for other entities (orgs, characters, etc)
    async def claim(self, ctx: ApplicationContext):
        """Send a form to the user to claim a playable entity and sends it to be approved by an admin"""
        
        if not io.load_approve_channel(ctx.guild_id):
            await ctx.respond("Error: A country approval channel has not been set!")
            return

        view = views.CountryAddView()
        await ctx.respond("Select an entity below and click the button to create a new country/entity.", view=view, ephemeral=True)
    
    @slash_command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for claim message to be sent in", required=False)
    async def send_claim_msg(self, ctx: ApplicationContext, channel: discord.TextChannel):
        """Admin command to send the claim message to a specific channel"""
        view = views.CountryAddView(timeout=None)
        if channel:
            await channel.send("Select an entity below and click the button to create a new country/entity.", view=view)
            await ctx.respond(f"Sent claim message to <#{channel.id}>!")
            return

        await ctx.respond("Select an entity below and click the button to create a new country/entity.", view=view)


    ### APPROVAL CHANNEL COMMANDS ###

    @approval_channelgroup.command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for countries awaiting approval to be posted")
    async def set(self, ctx: ApplicationContext, channel: discord.TextChannel) -> None:
        """Sets a channel for the approval queue"""

        io.save_approve_channel(channel.id, ctx.guild_id)
        await ctx.respond(f"Successfully set country approval channel to <#{channel.id}>.")

    @approval_channelgroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Gets the channel used for approvals"""

        channel = io.load_approve_channel(ctx.guild_id)
        if channel:
            await ctx.respond(f"The current approval channel is <#{channel}>.")
            return
            
        await ctx.respond("A country approval channel has not been set!")

    @approval_channelgroup.command()
    @has_permissions(administrator=True) # TODO: Raise error if there already is not one set.
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current approval queue channel"""

        if io.load_approve_channel(ctx.guild_id):
            io.save_approve_channel(None, ctx.guild_id)
            await ctx.respond("Successfully removed the country approval channel.")
            return

        await ctx.respond("A country approval channel has not been set!")

def setup(bot):
    bot.add_cog(Playable(bot))