import discord
from discord import option, ApplicationContext
import countrybot.io as io
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
    @option("year", description="RP Year")
    @option("month", description="RP Month (Default: Jan.)", default=1, required=False)
    @option("day", description="RP Day (Default: 1st of the month)", default=1, required=False)
    @option("sep", description="IRL days per in-RP year (Default: 2)", default=2, required=False)
    async def set(self, ctx: ApplicationContext, year: int, month: int, day: int, sep: float) -> None:
        """Sets the RP date."""
        
        rpdate = RPDate(year, month, day, sep)
        io.save_rpdate(rpdate, ctx.guild_id)

        await ctx.respond(f"Successfully set RP date to {rpdate}!")

    @dategroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Returns the current RP date."""

        await ctx.respond(f"The RP date is {io.load_rpdate(ctx.guild_id)}.")

        
def setup(bot):
    bot.add_cog(Date(bot))