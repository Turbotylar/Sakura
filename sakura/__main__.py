#Import all required libraries
from __future__ import unicode_literals
from sakura.models.guild import Guild
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import discord
from discord.ext import commands
import json

import logging
from fluent import handler as fluent_handler
logger = logging.getLogger(__name__)

# Setup logging
h = fluent_handler.FluentHandler("sakura.bot", host="fluentd", port=24224)
h.setFormatter(fluent_handler.FluentRecordFormatter({
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',
  'type': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}))
logging.basicConfig(level=logging.DEBUG, handlers=[h])



#Declare intents
intents = discord.Intents.default()
intents.members = True

#Get Prefix from config
def get_prefix(bot, message):
    prefixes = []
    prefixes.extend(bot.config["prefixes"])

    if message.guild is not None:
        db_session = bot.DBSession()
        guild = db_session.query(Guild).filter_by(discord_id=message.guild.id).first()
        db_session.close()
        if guild is not None and guild.custom_prefix is not None:
            prefixes.append(guild.custom_prefix)

    
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
    # Load config
    with open("config.json") as f:
        bot.config = json.load(f)

    # Setup DB
    engine = create_engine(bot.config["database_connection"], echo=True)

    bot.DBSession = sessionmaker(bind=engine)
    bot.db_engine = engine

    # Load cogs
    for ext in startup_cogs:
        try:
            bot.load_extension(ext)
        except Exception as e:
            logger.warning(f"Exception while loading {ext}: {e}")

    bot.run(bot.config["bot_api_key"])
    

