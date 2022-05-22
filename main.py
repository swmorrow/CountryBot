import os
import discord
from dotenv import load_dotenv
from countrybot.RPDate import DateNotSetError

initial_extensions = ['countrybot.cogs.date']
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
bot = discord.Bot()

if __name__ == '__main__':
     for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f'{bot.user} ~ Good morning, chat!')
    activity = discord.CustomActivity(name=f"over {69} countries", type=discord.ActivityType.watching) # Placeholder value for amount of countries
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error):
    if isinstance(error.original, DateNotSetError):
        return await ctx.respond("Error: No date set!")
    if ctx.command.name == "set" and ctx.cog.__cog_name__ == "Date":
        print(error.original)
        return await ctx.respond("Error: Invalid date!")
bot.run(os.getenv('TOKEN'))