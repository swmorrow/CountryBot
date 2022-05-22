import discord
from discord.commands import  SlashCommandGroup
from discord.ext import commands

class DateCog(commands.Cog):
    """A collection of the commands pertaining to the RP date.
    
            Attributes:
                bot: The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot

    dategroup = SlashCommandGroup("date", "Commands pertaining to the RP date")
    
    @dategroup.command()
    async def get(self, ctx):
        """Gets the current in-RP date"""
        await ctx.respond("Hello!")
        
def setup(bot):
    bot.add_cog(DateCog(bot))