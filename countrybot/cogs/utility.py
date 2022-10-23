import discord
from discord import option, ApplicationContext, Attachment
from discord.commands import SlashCommandGroup, slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions

import countrybot.utils.io as io
import countrybot.utils.embeds as emb
import countrybot.utils.imgurls as imgurls
import countrybot.views as views

from io import BytesIO

class Utility(commands.Cog):
    r"""A collection of utility commands.

    Attributes
    ------------
    bot: :class:`discord.Bot`
        The instance of the bot that is executing the commands.
    """

    def __init__(self, bot: discord.bot):
        self.bot = bot

    @slash_command()
    @option("flag", description="Image to be converted to a discord emoji-style flag")
    @option("aliasing", description="Aliasing of corners (accepted values betweeen 0 and 1)", required=False)
    async def flagify_file(self, ctx: ApplicationContext, flag: Attachment, aliasing: float = 0.7) -> None:
        with BytesIO() as image_binary:
            await imgurls.flagify_image(flag, aliasing, image_binary)
            await ctx.respond(file=discord.File(fp=image_binary, filename='flagified_image.png'))  

    @slash_command()
    @option("url", description="URL of image to be converted to a discord emoji-style flag")
    @option("aliasing", description="Aliasing of corners (accepted values betweeen 0 and 1)", required=False)
    async def flagify_url(self, ctx: ApplicationContext, url: str, aliasing: float = 0.7) -> None:
        with BytesIO() as image_binary:
            await imgurls.flagify_image(url, aliasing, image_binary)
            await ctx.respond(file=discord.File(fp=image_binary, filename='flagified_image.png'))

def setup(bot):
    bot.add_cog(Utility(bot))