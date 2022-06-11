import discord
from discord import option, ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

import countrybot.io as io
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
        io.save_rpdate(rpdate, ctx.guild_id)
        
        if rpdate.ticks != 1:
            advance = f"{rpdate.ticks} days!"
        else:
            advance = "day!"

        await ctx.respond(f"Successfully set RP date to {rpdate} with years advancing every " + advance)

    @dategroup.command()
    async def get(self, ctx: ApplicationContext) -> None:
        """Sends the current RP date."""

        await ctx.respond(f"The RP date is {io.load_rpdate(ctx.guild_id)}.")
    
    @dategroup.command()
    async def ticks_per_year(self, ctx: ApplicationContext) -> None:
        """Sends the amount of IRL days for each in-RP year."""

        rpdate = io.load_rpdate(ctx.guild_id)

        if rpdate.ticks != 1:
            advance = f"{rpdate.ticks} days."
        else:
            advance = "day."

        await ctx.respond(f"1 RP year advances every " + advance)


    ### CHANNEL COMMANDS ###

    @channelgroup.command()
    async def get(self, ctx: ApplicationContext):
        """Sends the channel that the date is currently set in."""

        channel = io.load_rpdate_channel(ctx.guild_id)

        if channel:
            await ctx.respond(f"The current date channel is <#{channel}>")
            return

        await ctx.respond(f"A date channel has not been set!")

    @channelgroup.command()
    @has_permissions(administrator=True)
    @option("channel", description="Channel for date updates to be posted")
    async def set(self, ctx: ApplicationContext, channel: discord.TextChannel) -> None:
        """Sets a channel for date advancements to be posted in every 24 hours."""

        io.save_rpdate_channel(channel.id, ctx.guild_id,)
        await ctx.respond(f"Successfully set date update channel to <#{channel.id}>.")

    @channelgroup.command()
    @has_permissions(administrator=True)
    async def remove(self, ctx: ApplicationContext) -> None:
        """Removes the current date advancement channel."""

        if io.load_rpdate_channel:
            io.save_rpdate_channel(None, ctx.guild_id)
            await ctx.respond("Successfully removed the date update channel.")
            return

        ctx.respond("A date channel has not been set!")
    

    ### LOOPING ###

    @tasks.loop(hours=24)
    async def advance_date(self):
        for guild_id in io.get_guilds():
            rpdate = io.load_rpdate(guild_id)
            rpdate_channel = io.load_rpdate_channel(guild_id)

            if rpdate is not None and rpdate_channel is not None:
                channel = await self.bot.fetch_channel(rpdate_channel)
                await channel.send(f"The RP date is {rpdate}.")

        
def setup(bot):
    bot.add_cog(Date(bot))