from sqlalchemy.orm.session import sessionmaker
import discord
from discord.ext import commands
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'


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
        self.Session = sessionmaker(bind=self.client.db_engine)

    
    async def check(self, ctx):
        await ctx.trigger_typing()

        db_session = self.Session()
        ctx.db_user = db_session.query(User).filter_by(discord_id=ctx.author.id).first()
        
        
        return True

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["bot_dev"]
            for role in ids
        )

    @commands.command(
        name='my_user'
    )
    async def my_user(self, ctx):
        """Returns my user instance"""
        await ctx.send(f"```\n{ctx.db_user}\n```")

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
    async def query(self, ctx, query: str):
        """Run a raw SQL query"""
        with self.client.db_engine.connect() as conn:
            rs = conn.execute(text(query))


        lines = "\n".join([' | '.join(row) for row in rs])
        await ctx.send(f"```sql\n{lines}\n```")

db_cog = None

def setup(bot):
    db_cog = Database(bot)
    bot.add_cog(db_cog)

    bot.add_check(db_cog.check)

def teardown(bot):
    bot.remove_check(db_cog.check)
