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

bind_database(get_secret("database", "connection"))
set_debug_guilds()


# Load cogs
for ext in startup_cogs:
    try:
        bot.load_extension(ext)
    except Exception as e:
        logger.warning(f"Exception while loading {ext}: {e}\n{traceback.format_exc()}")

bot.run(get_secret("discord", "bot_token"))



