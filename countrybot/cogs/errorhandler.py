import discord
from discord.ext import commands
import aiohttp
from pickle import PickleError
from PIL import UnidentifiedImageError, Image
import countrybot.utils.excepts as e
from countrybot.utils.embeds import error_embed
from traceback import print_exception

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
            
        if hasattr(ctx.command, 'on_error') or not isinstance(error.original, Exception):
            return
        
        match error:
            case commands.MissingPermissions():
                embed = error_embed("Invalid permissions!")
            
            case _:
                match error.original:
                    case e.ChannelNotSetError():
                        embed = error_embed("Channel not set!")

                    case e.DateNotSetError():
                        embed = error_embed("Date not set!")

                    case e.InvalidDateError():
                        embed = error_embed("Invalid date!")

                    case aiohttp.InvalidURL():
                        embed = error_embed("Invalid URL!")
                    
                    case Image.DecompressionBombError():
                        embed = error_embed("Image too large!")

                    case UnidentifiedImageError():
                        embed = error_embed("Invalid image!")

                    case PickleError():
                        embed = error_embed("Failed to (un)serialize")

                    case AttributeError():
                        embed = error_embed("No RPDate set!")

                    case _:
                        print(error)
                        print_exception(error.original)
                        embed = error_embed("Unknown error!")
        
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
            