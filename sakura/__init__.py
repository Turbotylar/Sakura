from sakura.utils.command import _update_permissions
from discord.commands.permissions import Permission
from sakura.models.user import User
from sakura.models.guild import Guild
from sakura.utils.secrets import get_secret
import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import logging
logger = logging.getLogger(__name__)

__version__ = "1.0.0"

USER_AGENT = f"Sakura/{__version__}"


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

#Setup bot with prefix and intents
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None)


#On startup log bots name and set presence
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Turbotylar/Sakura"))

@bot.event
async def on_connect():
    await sync_commands()


async def sync_commands():
    logger.info("Synchronizing commands")

    logger.debug("Searching for dev users & guilds")
    session = bot.DBSession()
    
    guilds = session.query(Guild).filter_by(is_debug_guild=True).all()
    guild_ids = [guild.discord_id for guild in guilds]

    users = session.query(User).filter_by(is_bot_dev=True).all()
    user_ids = [user.discord_id for user in users]

    session.close()

    logger.debug(f"Constructing dev permissions array")
    dev_permissions = [
        Permission(user, 2, True, guild)
        for user in user_ids
        for guild in guild_ids
    ]

    logger.debug(f"Updating permissions on commands")

    

    for cmd in bot.pending_application_commands + bot.application_commands:
        _update_permissions(cmd, dev_permissions=dev_permissions)


    logger.debug(f"Syncing with discord")
    await bot.register_commands()

def bind_database(connection_string):
    engine = create_engine(connection_string)

    bot.DBSession = sessionmaker(bind=engine)
    bot.db_engine = engine

def set_debug_guilds():
    db_session = bot.DBSession()
    guilds = db_session.query(Guild).filter_by(is_debug_guild=True).all()
    db_session.close()
    debug_guild_ids = [guild.discord_id for guild in guilds]
    
    if len(debug_guild_ids) > 0:
        logger.info(f"Setting debug guilds to {debug_guild_ids}")
        bot.debug_guilds = debug_guild_ids
    else:
        logger.info(f"Deploy all commands globally")
