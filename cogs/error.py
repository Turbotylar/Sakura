import discord
import traceback
import sys
from discord.ext import commands

class ErrorCog(commands.Cog, name="Error Handler"):
    """
    Handles errors that may occur
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(ErrorCog(bot))


