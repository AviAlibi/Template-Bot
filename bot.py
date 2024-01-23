import discord
from discord.ext import commands
# from asyncpg import create_pool
from os import getenv
from logging import INFO, basicConfig, info, FileHandler, StreamHandler

basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[
            FileHandler("bot_debug.log"), StreamHandler()])
# THIS IS USED FOR LOGGING
# INSTEAD OF PRINT, YOU CAN DO "FROM LOGGING IMPORT ERROR, INFO"
# INFO("STRING TEXT")
# ERROR("ERROR TEXT")
# ALL LOGGING WILL BE SAVED INTO BOT_DEBUG.LOG FILE

# here I import all intents because I am lazy, but actual on/offs are available
intents = discord.Intents.all()
# intents.guilds = True
# intents.members = True
# intents.presences = True
# intents.voice_states = True
# intents.message_content = True
# intents.messages = True
# intents.reactions = True
# intents.guild_messages = True
# intents.dm_messages = True
# intents.invites = True

bot = commands.Bot(intents=intents, status=discord.Status.idle, command_prefix=getenv(
    'PREFIX'), activity=discord.Game(name="Booting"))

# REMOVES FAULT HELP COMMAND. YOU CAN CREATE YOUR OWN HELP COMMAND THE SAME WAY YOU WOULD MAKE A NORMAL COMMAND
bot.remove_command("help")


@bot.event
async def on_ready():
    info('\x1b[0;30;44m' +
         f'Logged in as {bot.user.name}' + '\x1b[0m' + '\n    ----------')
    info('\x1b[6;30;42m' + 'Bot - Online' + '\x1b[0m' + '\n')
    await bot.change_presence(status=discord.Status.online)

    # WILL PUSH ALL NEW COMMANDS AUTOMATICALLY
    await bot.wait_until_ready()
    await bot.tree.sync()

# THIS IS WHERE YOU RUN STUFF YOU WANT TO DO ON STARTUP, DON'T DO IT IN ON_READY


@bot.event
async def setup_hook():
    # this will be every cog file and its commands that are within this list, this lets you remove and add files as you want and not just running every file in the folder, more work, easier debugging
    active_extensions = ['cogs._example_cog']
    if __name__ == '__main__':
        # this is basically loading the files
        for extension in active_extensions:
            await bot.load_extension(extension)  # LOADS THE EXTENSION

    # ENABLE IF USING A POSTGRES DATABASE. MAKE SURE TO EDIT ALL ENV VALUES
    # bot.pg_con = await create_pool(host=getenv('DB_HOST'), port=getenv('DB_PORT'), database=getenv('DB_NAME'), user=getenv('DB_USER'), password=getenv('DB_PASSWORD'))

# this will run the actual discord bot
bot.run(getenv('token'))
