import discord
from discord.ext import commands
from run import bot


class DateCog(commands.Cog):
    """ A collection of the commands pertaining to the RP date.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    async def hello(ctx):
        """Hello!"""
        await ctx.respond("Hello!")
        
def setup(bot):
    bot.add_cog(DateCog(bot))