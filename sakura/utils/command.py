"""Custom decorator for defining commands, with special options."""

from discord.ext import commands
from sakura.utils.database import attach_database_guild, attach_database_user, database_connect
import sakura.utils.logger
import logging
logger = logging.getLogger(__name__)


def sakura_command(
        parent = commands.command,
        *args,
        connect_database=False,
        attach_user=False,
        attach_guild=False,
        attach_logger=True,
        **kwargs):

    parent_setup = parent(*args, **kwargs)

    def decorator(func):
        
        logger.info(f"Registering command {func} with options\n\t" + "\n\t".join([
            f"{connect_database = }",
            f"{attach_user = }",
            f"{attach_guild = }",
            f"{attach_logger = }",
        ]))

        func = parent_setup(func)
        
        if connect_database or attach_guild or attach_user:
            func = database_connect(func)

        if attach_user:
            func = attach_database_user(func)

        if attach_guild:
            func = attach_database_guild(func)
        
        if attach_logger:
            func = sakura.utils.logger.attach_logger(func)

        return func

    return decorator