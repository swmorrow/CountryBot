import discord
from discord.commands import  SlashCommandGroup
from discord.ext import commands

class DateCog(commands.Cog):
    """A collection of the commands pertaining to the RP date."""
    
    def __init__(self, bot):
        self.bot = bot

    dategroup = SlashCommandGroup("date", "Commands pertaining to the RP date")
    
    @dategroup.command()
    async def hello(self, ctx):
        """Hello!"""
        await ctx.respond("Hello!")
        
def setup(bot):
    bot.add_cog(DateCog(bot))