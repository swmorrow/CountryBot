import discord
import countrybot.utils as utils
from countrybot.RPDate import RPDate
from discord import option
from discord.commands import SlashCommandGroup
from discord.ext import commands


class Date(commands.Cog):
    """A collection of the commands pertaining to the RP date.
    
            Attributes:
                bot: The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot

    dategroup = SlashCommandGroup("date", "Commands pertaining to the RP date")
    
    @dategroup.command()
    @option("date", description="Date in zero-leading YYYY-MM-DD format (ex. 1991-05-21)")
    @option("sep", description="IRL days per in-RP year", default=2, required=False)
    async def set(self, ctx: discord.ApplicationContext, date: str, sep: float) -> None:
        """Sets the RP date in zero-leading YYYY-MM-DD format."""
        rpdate = RPDate(date, sep)
        utils.save_rpdate(rpdate)
        pickled_rpdate = utils.load_rpdate()
        if pickled_rpdate.get_date() != rpdate.get_date():
            print("Error (un?)pickling rpdate.")
            raise Exception
        await ctx.respond(f"Successfully set RP date to {pickled_rpdate}!")

    @dategroup.command()
    async def get(self, ctx: discord.ApplicationContext) -> None:
        """Returns the current RP date."""
        await ctx.respond(f"The RP date is {utils.load_rpdate()}.")

        
def setup(bot):
    bot.add_cog(Date(bot))