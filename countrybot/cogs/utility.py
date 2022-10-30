import discord
from discord.commands import slash_command
from discord.ext import commands

import countrybot.utils.imgurls as imgurls
import countrybot.utils.embeds as emb

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
    @discord.option("file", description="File to be converted to a discord emoji-style flag", required=False)
    @discord.option("url", description="URL of image to be converted to a discord emoji-style flag", required=False)
    async def flagify(self, ctx: discord.ApplicationContext, file: discord.Attachment, url: str) -> None:
        """Takes an image and removes the corners, converting it into the style of a Discord flag emoji."""
        if file is None and url is None:
            await ctx.respond(embed=emb.error_embed("No flag specified!"))
            return

        await ctx.response.defer()

        if file is None:
            flagified_img = await imgurls.flagify_image(url)

        else: # TODO: currently, if both are specified, it only returns the file. This should be fixed/signposted
            flagified_img = await imgurls.flagify_image(file)

        with BytesIO() as output:
            flagified_img.save(output, format="PNG")
            output.seek(0)

            await ctx.followup.send(file=discord.File(fp=output, filename='flagified_image.png'))

def setup(bot):
    bot.add_cog(Utility(bot))