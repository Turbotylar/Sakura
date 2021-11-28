from __future__ import unicode_literals
from discord.commands.commands import SlashCommand

from discord.commands.permissions import Permission
from discord.interactions import Interaction
from sakura.models.user import User
from sakura.utils.secrets import get_secret
from sakura.models.guild import Guild
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import discord
from discord.ext import commands
import traceback
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.WARNING)
logging.getLogger("sakura").setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

def get_prefix(bot, message):
    prefixes = []
    prefixes.append(get_secret("discord", "prefix"))

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
    "sakura.cogs.misc",
    "sakura.cogs.interactions",
    "sakura.cogs.moderation",
    "sakura.cogs.help",
    "sakura.cogs.glance",
    "sakura.cogs.search",
    "sakura.cogs.guild",
]

#Setup bot with prefix and intents
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None)

async def sync_commands():
    logger.info("Synchronizing commands")

    logger.debug("Searching for dev users & guilds")
    session = bot.DBSession()
    
    guilds = db_session.query(Guild).filter_by(is_debug_guild=True).all()
    guild_ids = [guild.discord_id for guild in guilds]
    logger.debug(f"Got guild ids {guild_ids}")

    users = db_session.query(User).filter_by(is_bot_dev=True).all()
    user_ids = [user.discord_id for user in users]
    logger.debug(f"Got user ids {user_ids}")

    session.close()

    logger.debug(f"Constructing permissions array")
    dev_permissions = [
        Permission(user, 2, True, guild)
        for user in user_ids
        for guild in guild_ids
    ]

    logger.debug(f"Stripping any commands with parents")

    bot._pending_application_commands = [
        cmd for cmd in bot.pending_application_commands
        if hasattr(cmd, "parent") and cmd.parent is None
        ]

    logger.debug(f"Searching for dev commands")

    

    for cmd in bot.application_commands + bot.pending_application_commands:
        logger.debug(f"Checking {cmd}")

        if hasattr(cmd, "callback") and hasattr(cmd.callback, "dev_command") and cmd.callback.dev_command == True:
            logger.debug(f"Found {cmd} to be dev command")
            cmd.guild_ids = guild_ids.copy()
            cmd.default_permission = False
            cmd.permissions = dev_permissions.copy()

    logger.debug(f"Syncing with discord")
    await bot.register_commands()




#On startup log bots name and set presence
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Turbotylar/Sakura"))

@bot.event
async def on_connect():
    await sync_commands()

#Load Extentions and commands
if __name__ == "__main__":
    # Setup DB
    engine = create_engine(get_secret("database", "connection"))

    bot.DBSession = sessionmaker(bind=engine)
    bot.db_engine = engine

    db_session = bot.DBSession()
    guilds = db_session.query(Guild).filter_by(is_debug_guild=True).all()
    db_session.close()
    debug_guild_ids = [guild.discord_id for guild in guilds]
    
    if len(debug_guild_ids) > 0:
        logger.info(f"Setting debug guilds to {debug_guild_ids}")
        bot.debug_guilds = debug_guild_ids
    else:
        logger.info(f"Deploy all commands globally")


    # Load cogs
    for ext in startup_cogs:
        try:
            bot.load_extension(ext)
        except Exception as e:
            logger.warning(f"Exception while loading {ext}: {e}\n{traceback.format_exc()}")

    bot.run(get_secret("discord", "bot_token"))
    


