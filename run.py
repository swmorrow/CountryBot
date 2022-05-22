import discord

initial_extensions = ['countrybot.commands.date']
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot()

if __name__ == '__main__':
     for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f'{bot.user} ~ Starting up...')
    activity = discord.CustomActivity(name=f"over {69} countries", type=discord.ActivityType.watching) # Placeholder value for amount of countries
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run('OTc3NjU0Nzk1MjE5MzkwNTQ1.G2ulv_.zNsQc5orIJr1B9_oiDLW57D_bADwYjp58gkt5o')