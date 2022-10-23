import os, discord, logging
import countrybot.utils.io as io
from countrybot.configparser import LOG_FILE
from dotenv import load_dotenv


bot = discord.Bot()

initial_extensions = ['countrybot.cogs.date', 'countrybot.cogs.errorhandler', 'countrybot.cogs.country', 'countrybot.cogs.utility']
intents = discord.Intents.default()
intents.members = True

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

@bot.event
async def on_ready():
    print(f'{bot.user} ~ Good morning, chat!')
    
    activity = discord.Activity(
        name=f"over your countries",
        type=discord.ActivityType.watching,
    )
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
async def on_application_command(ctx: discord.ApplicationContext):
    print(f"{ctx.user} ~ used /{ctx.command} in {ctx.guild.name} (id: {ctx.guild.id})")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f'{bot.user} ~ Joined {guild.name} (id: {guild.id})')
    io.register(guild.id)

@bot.event
async def on_guild_remove(guild: discord.Guild):
    print(f'{bot.user} ~ Left {guild.name} (id: {guild.id}) :(')
    io.unregister(guild.id)

bot.run(os.getenv('TOKEN'))