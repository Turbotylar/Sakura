from __future__ import unicode_literals
from sakura.utils.secrets import get_secret
import traceback
from sakura import bind_database, set_debug_guilds, bot
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.WARNING)
logging.getLogger("sakura").setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)


#List of cogs
startup_cogs = [
    "sakura.bot.cogs.database",
    "sakura.bot.cogs.error",
    "sakura.bot.cogs.manage",
    "sakura.bot.cogs.misc",
    "sakura.bot.cogs.interactions",
    "sakura.bot.cogs.moderation",
    "sakura.bot.cogs.help",
    "sakura.bot.cogs.glance",
    "sakura.bot.cogs.search",
    "sakura.bot.cogs.guild",
    "sakura.bot.cogs.musicquiz",
    "sakura.bot.cogs.socialcredit",
]

bind_database(get_secret("database", "connection"))
set_debug_guilds()


# Load cogs
for ext in startup_cogs:
    try:
        bot.load_extension(ext)
    except Exception as e:
        logger.warning(f"Exception while loading {ext}: {e}\n{traceback.format_exc()}")

bot.run(get_secret("discord", "bot_token"))



