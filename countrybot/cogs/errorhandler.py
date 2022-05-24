import discord
from discord.ext import commands
from countrybot.cogs.date import Date
from countrybot.rpdate import DateNotSetError
from pickle import PickleError

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: commands.CommandError) -> None:
        r"""The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: :class:`commands.Context`
            The context used for command invocation.
        error: :class:`commands.CommandError`
            The Exception raised.
        """

        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("Error: Invalid permissions!", ephemeral=True)
            return
            
        if hasattr(ctx.command, 'on_error') or not isinstance(error.original, Exception):
            return
        
        print(error)

        if isinstance(ctx.cog, Date): # Date cog exceptions

            if isinstance(error.original, DateNotSetError):
                await ctx.respond("Error: No date set!", ephemeral=True)
                return

            if ctx.command.name == "set" and isinstance(error.original, ValueError):
                await ctx.respond(f"Error: Invalid date!")
                return

            if isinstance(error.original, PickleError):
                await ctx.respond("Error: RPDate failed to (un)serialize", ephemeral=True)
                return

            if isinstance(error.original, AttributeError):
                await ctx.respond("Error: no RPDate set!", ephemeral=True)
                return 
        

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
            