import os
import discord
from dotenv import load_dotenv

initial_extensions = ['countrybot.cogs.date', 'countrybot.cogs.errorhandler']
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
    activity = discord.Activity(name=f"over {69} countries", type=discord.ActivityType.watching) # Placeholder value for amount of countries
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run(os.getenv('TOKEN'))