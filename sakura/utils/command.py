"""Custom decorator for defining commands, with special options
"""

from discord.ext import commands
from sakura.utils.database import attach_database_guild, attach_database_user, database_connect


def sakura_command(
    parent = commands.command,
    *args,
    connect_database=False,
    attach_user=False,
    attach_guild=False,
    **kwargs):

    if attach_guild or attach_user:
        connect_database = True

    if connect_database: parent = database_connect(parent)
    if attach_user: parent = attach_database_user(parent)
    if attach_guild: parent = attach_database_guild(parent)

    return parent(*args, **kwargs)