import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup, slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions

import countrybot.utils.io as io
import countrybot.utils.embeds as emb
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

    approval_channelgroup = SlashCommandGroup("approval_channel", "Commands pertaining to the country approval channel")

    @slash_command()
    async def claim(self, ctx: ApplicationContext) -> None:
        """Send a form to the user to claim a playable entity and sends it to be approved by an admin"""
        
        io.load_approve_channel(ctx.guild_id) # check if a channel is already set

        view = views.CountryAddView()
        await ctx.respond("Select an entity below and click the button to create a new country/entity.", view=view, ephemeral=True)


    ### APPROVAL CHANNEL COMMANDS ###

    @approval_channelgroup.command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for countries awaiting approval to be posted")
    async def set(self, ctx: ApplicationContext, channel: discord.TextChannel) -> None:
        """Sets a channel for the approval queue"""

        io.save_approve_channel(channel.id, ctx.guild_id)
        await ctx.respond(embed=emb.success_embed(f"Set country approval channel to <#{channel.id}>."))

    @approval_channelgroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Gets the channel used for approvals"""

        channel = io.load_approve_channel(ctx.guild_id)
        await ctx.respond(embed=emb.msg_embed(f"The current approval channel is <#{channel}>."))
            
    @approval_channelgroup.command()
    @has_permissions(administrator=True)
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current approval queue channel"""

        io.load_approve_channel(ctx.guild_id)
        io.save_approve_channel(None, ctx.guild_id)
        await ctx.respond(embed=emb.success_embed("Removed the country approval channel."))

def setup(bot):
    bot.add_cog(Playable(bot))