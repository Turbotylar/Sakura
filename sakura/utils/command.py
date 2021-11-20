"""Custom decorator for defining commands, with special options
"""

from discord.ext import commands
from sakura.utils.database import attach_database_guild, attach_database_user, database_connect
import logging
logger = logging.getLogger(__name__)


def sakura_command(
        parent = commands.command,
        *args,
        connect_database=False,
        attach_user=False,
        attach_guild=False,
        **kwargs):

    parent_setup = parent(*args, **kwargs)

    def decorator(func):
        
        logger.info(f"Registering command {func}", {
            "custom_options": {
                "connect_database": connect_database,
                "attach_user": attach_user,
                "attach_guild": attach_guild
            },
            "options": kwargs
        })


        func = parent_setup(func)
        

        if connect_database or attach_guild or attach_user:
            func = database_connect(func)

        if attach_user:
            func = attach_database_user(func)

        if attach_guild:
            func = attach_database_guild(func)

        return func

    return decorator
    