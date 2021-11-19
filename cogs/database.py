import discord
from discord.ext import commands
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GuildUser(Base):
    __tablename__ = 'guilduser'


    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    is_bot_dev = Column(Boolean)


    def __repr__(self) -> str:
        return f"<User(id={self.id}, discord_id={self.discord_id}, is_bot_dev={self.is_bot_dev})>"

class Database(commands.Cog, name="Database"):
    """
    Database management commands
    """
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["bot_dev"]
            for role in ids
        )

    @commands.command(
        name='sync',
    )
    async def sync(self, ctx):
        """Sync database schema with database"""

        Base.metadata.create_all(self.client.db_engine)

        await ctx.send('Database synced')

    @commands.command(
        name='query'
    )
    async def query(self, ctx, *query: str):
        """Run a raw SQL query"""
        with self.client.db_engine.connect() as conn:
            rs = conn.execute(query)

        await ctx.send(f"```sql\n{rs}\n```")



def setup(bot):
    bot.add_cog(Database(bot))
