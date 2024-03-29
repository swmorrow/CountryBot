import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

import datetime as dt
from countrybot.utils.excepts import RPDateNotPostedError

import countrybot.utils.io as io
import countrybot.utils.embeds as emb
from countrybot.rpdate import RPDate

class Date(commands.Cog):
    r"""A collection of the commands pertaining to the RP date.

    Attributes
    ------------
    bot: :class:`discord.Bot`
        The instance of the bot that is executing the commands.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.advance_date.start()

    dategroup = SlashCommandGroup("date", "Commands pertaining to the RP date")
    
    channelgroup = dategroup.create_subgroup("channel", "Commands pertaining to the RP date channel")


    ### GENERAL COMMANDS ###
    
    @dategroup.command()
    @has_permissions(administrator=True)
    @option("year", description="RP Year")
    @option("month", description="RP Month (Default: Jan.)", default=1, required=False)
    @option("day", description="RP Day (Default: 1st of the month)", default=1, required=False)
    @option("ticks_per_day", description="IRL days per in-RP year (Default: 2)", default=2, required=False)
    async def set(self, ctx: ApplicationContext, year: int, month: int, day: int, ticks_per_day: float) -> None:
        """Sets the RP date."""

        rpdate = RPDate(year, month, day, ticks_per_day)
        await io.save_rpdate(rpdate, ctx.guild_id)
        
        if rpdate.ticks != 1:
            advance = f"{rpdate.ticks} days!"
        else:
            advance = "day!"

        await ctx.respond(embed=emb.success_embed(f"Set RP date to {rpdate} with years advancing every {advance}"))

    @dategroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Sends the current RP date."""

        await ctx.respond(embed=discord.Embed(title=f"The RP date is {await io.load_rpdate(ctx.guild_id)}.", color=discord.Color.blurple()))

    @dategroup.command()
    @has_permissions(administrator=True)
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current RP date."""

        await io.load_rpdate(ctx.guild_id) # check if date is set already
        await io.save_rpdate(None, ctx.guild_id)
        await ctx.respond(embed=emb.success_embed(f"Removed the RP date."))
    
    @dategroup.command()
    async def ticks_per_year(self, ctx: ApplicationContext) -> None:
        """Sends the amount of IRL days for each in-RP year."""

        rpdate = await io.load_rpdate(ctx.guild_id)

        if rpdate.ticks != 1:
            advance = f"{rpdate.ticks} days."
        else:
            advance = "day."

        await ctx.respond(embed=emb.msg_embed(f"1 RP year advances every " + advance))


    ### CHANNEL COMMANDS ###

    @channelgroup.command()
    async def get(self, ctx: ApplicationContext):
        """Sends the channel that the date is currently set in."""

        channel = await io.load_rpdate_channel(ctx.guild_id)
        await ctx.respond(embed=emb.msg_embed(f"The current date channel is <#{channel}>."))

    @channelgroup.command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for date updates to be posted")
    async def set(self, ctx: ApplicationContext, channel: discord.TextChannel) -> None:
        """Sets a channel for date advancements to be posted in every 24 hours."""

        await io.save_rpdate_channel(channel.id, ctx.guild_id,)
        await ctx.respond(embed=emb.success_embed(f"Set date update channel to <#{channel.id}>."))

    @channelgroup.command()
    @has_permissions(administrator=True)
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current date advancement channel."""

        await io.load_rpdate_channel(ctx.guild_id) # check if rpdate channel is set
        await io.save_rpdate_channel(None, ctx.guild_id)
        await ctx.respond(embed=emb.success_embed("Removed the date update channel."))

    ### LOOPING ###

    @tasks.loop(minutes=30) # make this lower if it doesnt affect performance
    async def advance_date(self):
        for guild_id in await io.get_guilds():
            try:
                rpdate = await io.load_rpdate(guild_id)
                channel_id = await io.load_rpdate_channel(guild_id)
                guild_channel = await self.bot.fetch_channel(channel_id)
                last_posting = await io.load_last_rpdate_posting(guild_id)

                if dt.datetime.now() - last_posting > dt.timedelta(days=1):
                    await guild_channel.send(embed=discord.Embed(title=f"The RP date is {rpdate}.", color=discord.Color.blurple()))
                    await io.save_last_rpdate_posting(dt.datetime.now(), guild_id)

            except Exception as e:
                if isinstance(e, RPDateNotPostedError):
                    await guild_channel.send(embed=discord.Embed(title=f"The RP date is {rpdate}.", color=discord.Color.blurple())) 

                    await io.save_last_rpdate_posting(dt.datetime.now(), guild_id)
        
def setup(bot):
    bot.add_cog(Date(bot))