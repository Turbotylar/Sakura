"""Simple, reusable checks for commands
"""

import discord
from discord.ext import commands
from sakura.utils.database import get_database_session, get_guild, get_user


def is_bot_dev():
    async def predicate(ctx):
        user = await get_user(await get_database_session(ctx), ctx.author.id)
        return user.is_bot_dev

    return commands.check(predicate)

def is_guild_moderator():
    async def predicate(ctx):
        if ctx.guild is None:
            return False # Guild-only command

        guild = await get_guild(await get_database_session(ctx), ctx.guild.id)

        return guild.mod_role in [role.id for role in ctx.author.roles]

    return commands.check(predicate)