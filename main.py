import os, discord, config
import countrybot.io as io
from dotenv import load_dotenv

initial_extensions = ['countrybot.cogs.date', 'countrybot.cogs.errorhandler', 'countrybot.cogs.country']
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
bot = discord.Bot()

if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.DATA_DIRECTORY =  os.path.join(config.ABSOLUTE_PATH, os.path.dirname(config.DATA_DIRECTORY + '\\'))
    config.DATABASE = os.path.join(config.DATA_DIRECTORY, 'country_database.db')

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f'{bot.user} ~ Good morning, chat!')
    activity = discord.Activity(name=f"over {io.get_num_countries()} countries", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    bot_guilds = set([guild.id for guild in bot.guilds])
    registered_guilds = set(io.get_guilds())

    guilds_joined = list(bot_guilds.difference(registered_guilds))
    guilds_left = list(registered_guilds.difference(bot_guilds))

    if len(guilds_joined) != 0:
        print('Guilds joined since last episode...')

        for guild in guilds_joined:
            io.register(guild)
            guild = await bot.fetch_guild(guild)
            print(f'- {bot.user} ~ Joined {guild.name} (id: {guild.id})')

    if len(guilds_left) != 0:
        print('Guilds left since last episode...')

        for guild in guilds_left:
            io.unregister(guild)
            print(f'- {bot.user} ~ Left guild (id: {guild}) :(')

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f'{bot.user} ~ Joined {guild.name} (id: {guild.id})')
    io.register(guild.id)

@bot.event
async def on_guild_remove(guild: discord.Guild):
    print(f'{bot.user} ~ Left {guild.name} (id: {guild.id}) :(')
    io.unregister(guild.id)

bot.run(os.getenv('TOKEN'))