from sakura.models.guild import Guild
from sakura.models.user import User

import logging
logger = logging.getLogger(__name__)

#
#   Custom Hooks 
#
def get_hooks(hook_dict):
    before = []
    after = []

    async def db_connect_before(cog, ctx):
        ctx.db_session = await get_database_session(ctx)
        logger.debug("Connected to database")

    async def db_connect_after(cog, ctx):
        logger.debug("Commiting database changes")
        ctx.db_session.commit()
        ctx.db_session.close()
        ctx.db_session = None
        logger.debug("Commited database changes")
    
    async def db_user_before(cog, ctx):
        logger.debug("Getting user from database")
        ctx.db_user = await get_user(ctx.db_session, ctx.author.id)

    async def db_guild_before(cog, ctx):
        logger.debug("Getting guild from database")

        ctx.db_guild = await get_guild(ctx.db_session, ctx.guild.id)

    if hook_dict["attach_user"] or hook_dict["attach_guild"] or hook_dict["connect_database"]:
        before.append(db_connect_before)
        after.append(db_connect_after)

    if hook_dict["attach_user"]:
        before.append(db_user_before)

    if hook_dict["attach_guild"]:
        before.append(db_guild_before)

    return (before, after)
    
#
#   Useful helper methods
#

async def get_user(session, discord_id):
    user = session.query(User).filter_by(discord_id=discord_id).first()

    if user is None:
        user = User(discord_id=discord_id)
        session.add(user)

    return user


async def get_guild(session, discord_id):
    guild = session.query(Guild).filter_by(discord_id=discord_id).first()

    if guild is None:
        guild = Guild(discord_id=discord_id)
        session.add(guild)

    return guild


async def get_database_session(context):   
    context.db_session = context.bot.DBSession()
    return context.db_session