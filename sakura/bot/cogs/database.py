from sakura.bot.utils.command import sakura_command
from discord.commands.context import ApplicationContext
from discord.ext import commands
from sqlalchemy import text
import logging
logger = logging.getLogger(__name__)


class Database(commands.Cog, name="Database"):
    """
    Database management commands
    """
    def __init__(self, client):
        self.client = client

    @sakura_command(
        attach_user=True
    )
    async def my_user(self, ctx: ApplicationContext):
        """Returns my user instance"""
        await ctx.respond(f"```\n{ctx.db_user}\n```")
        

    @sakura_command(
        connect_database=True,
        dev_command = True
        
    )
    async def query(self, ctx: ApplicationContext, query: str):
        """Run a raw SQL query"""
        rs = ctx.db_session.execute(text(query))

        lines = " | ".join(rs.keys()) + "\n%s\n"
        lines += "\n".join([' | '.join(map(str,row)) for row in rs])
        lines = lines % ("=" * max([len(line) for line in lines.split("\n")]))

        await ctx.respond(f"```sql\n{lines}\n```")


def setup(bot):
    bot.add_cog(Database(bot))
    
