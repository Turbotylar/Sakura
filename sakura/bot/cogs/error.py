from discord.commands.context import ApplicationContext
from discord.commands.errors import ApplicationCommandInvokeError
from discord.embeds import Embed
from discord.ext import commands
import traceback

class ErrorCog(commands.Cog, name="Error Handler"):
    """
    Handles errors that may occur
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext, err: Exception):
        embed = Embed(color= 0xeb4034, title="Error", description="There was an error while processing your request\nIf you know what your doing, the error details are below")

        if isinstance(err, ApplicationCommandInvokeError):
            err = err.original
            
        embed.add_field(name=err.__class__.__name__, value=str(err))
        try:
            raise err
        except BaseException:
            traceback.print_exc()

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ErrorCog(bot))