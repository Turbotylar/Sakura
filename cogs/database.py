from sqlalchemy.orm.session import sessionmaker
import discord
from discord.ext import commands
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    is_bot_dev = Column(Boolean, default=False)


    def __repr__(self) -> str:
        return f"<User(id={self.id}, discord_id={self.discord_id}, is_bot_dev={self.is_bot_dev})>"

class Database(commands.Cog, name="Database"):
    """
    Database management commands
    """
    def __init__(self, client):
        self.client = client
        self.Session = sessionmaker(bind=self.client.db_engine)

    async def database_connect(self, ctx):
        db_session = self.Session()
        ctx.db_session = db_session
        ctx.db_user = db_session.query(User).filter_by(discord_id=ctx.author.id).first()

        if ctx.db_user is None:
            ctx.db_user = User(discord_id=ctx.author.id)
            db_session.add(ctx.db_user)
            ctx.db_session.commit()

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

    @commands.before_invoke(database_connect)
    @commands.command(
        name='my_user'
    )
    async def my_user(self, ctx):
        """Returns my user instance"""
        await ctx.send(f"```\n{ctx.db_user}\n```")

    @commands.before_invoke(database_connect)
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
    Base.metadata.create_all(bot.db_engine)
    bot.add_cog(Database(bot))
