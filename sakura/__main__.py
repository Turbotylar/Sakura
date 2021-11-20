#Import all required libraries
from __future__ import unicode_literals
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import discord
from discord.ext import commands
import json
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


#Declare intents
intents = discord.Intents.default()
intents.members = True

#Get Prefix from config
def get_prefix(bot, message):
    prefixes = bot.config["prefixes"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

#List of cogs
startup_cogs = [
    "sakura.cogs.database",
    "sakura.cogs.error",
    "sakura.cogs.manage",
    "sakura.cogs.reddit",
    "sakura.cogs.tenor",
    "sakura.cogs.misc",
    "sakura.cogs.interactions",
    "sakura.cogs.moderation",
    "sakura.cogs.help",
    "sakura.cogs.glance"
]

#Setup bot with prefix and intents
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

#On startup log bots name and set presence
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Turbotylar/Sakura"))

#Load Extentions and commands
if __name__ == "__main__":
    for ext in startup_cogs:
        try:
            bot.load_extension(ext)
        except Exception as e:
            logger.warning(f"Exception while loading {ext}: {e}")

    # Load config
    with open("config.json") as f:
        bot.config = json.load(f)

    # Setup DB
    engine = create_engine(bot.config["database_connection"], echo=True)

    bot.DBSession = sessionmaker(bind=engine)
    bot.db_engine = engine

    bot.run(bot.config["bot_api_key"])
    
