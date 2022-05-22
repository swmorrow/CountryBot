import discord
from discord import option, ApplicationContext
import countrybot.utils as utils
from countrybot.RPDate import RPDate
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import has_permissions


class Date(commands.Cog):
    r"""A collection of the commands pertaining to the RP date.

    Attributes
    ------------
    bot: :class:`discord.Bot` The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot

    dategroup = SlashCommandGroup("date", "Commands pertaining to the RP date")
    
    @dategroup.command()
    @has_permissions(administrator=True)
    @option("date", description="Date in zero-leading YYYY-MM-DD format (ex. 1991-05-21)")
    @option("sep", description="IRL days per in-RP year (Default: 2)", default=2, required=False)
    async def set(self, ctx: ApplicationContext, date: str, sep: float) -> None:
        """Sets the RP date in zero-leading YYYY-MM-DD format."""
        
        rpdate = RPDate(date, sep)
        utils.save_rpdate(rpdate)

        await ctx.respond(f"Successfully set RP date to {rpdate}!")

    @dategroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Returns the current RP date."""

        await ctx.respond(f"The RP date is {utils.load_rpdate()}.")

        
def setup(bot):
    bot.add_cog(Date(bot))