"""Simple, reusable checks for commands."""

import discord
from discord.ext import commands
from sakura.utils.database import get_database_session, get_guild, get_user


def is_bot_dev():
    async def predicate(ctx):

        db = await get_database_session(ctx)
        user = await get_user(db, ctx.author.id)
        db.close()

        return user.is_bot_dev

    return commands.check(predicate)


def is_guild_moderator():
    async def predicate(ctx):
        if ctx.guild is None:
            return False # Guild-only command

        db = await get_database_session(ctx)
        guild = await get_guild(db, ctx.guild.id)
        db.close()
        
        return guild.mod_role in [role.id for role in ctx.author.roles]

    return commands.check(predicate)