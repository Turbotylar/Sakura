"""Simple, reusable checks for commands
"""

import discord
from discord.ext import commands
from utils.database import get_user


def is_bot_dev():
    async def predicate(ctx):
        user = await get_user(ctx.bot.DBSession(), ctx.author.id)
        return user.is_bot_dev

    return commands.check(predicate)