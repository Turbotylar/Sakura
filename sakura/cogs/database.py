import discord
from discord.ext import commands
from models.base import Base as DatabaseBase
from utils.checks import is_bot_dev
from utils.database import attach_database_user, database_connect, get_user
from sqlalchemy import text


class Database(commands.Cog, name="Database"):
    """
    Database management commands
    """
    def __init__(self, client):
        self.client = client
        
    @is_bot_dev()
    @commands.command(
        name='sync',
    )
    async def sync(self, ctx):
        """Sync database schema with database"""

        DatabaseBase.metadata.create_all(self.client.db_engine)
        await ctx.send('Database synced')

    @database_connect
    @attach_database_user
    @commands.command(
        name='my_user'
    )
    async def my_user(self, ctx):
        """Returns my user instance"""
        await ctx.send(f"```\n{ctx.db_user}\n```")

    @is_bot_dev()
    @database_connect
    @commands.command(
        name='query'
    )
    async def query(self, ctx, query: str):
        """Run a raw SQL query"""
        rs = ctx.db_session.execute(text(query))

        lines = " | ".join(rs.keys()) + "\n%s\n"
        lines += "\n".join([' | '.join(map(str,row)) for row in rs])
        lines = lines % ("=" * max([len(line) for line in lines.split("\n")]))
        await ctx.send(f"```sql\n{lines}\n```")

def setup(bot):
    bot.add_cog(Database(bot))
