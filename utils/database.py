from models.user import User

import logging

from utils.hooks import before_invoke_hook, after_invoke_hook
logger = logging.getLogger(__name__)

#
#   Custom Hooks 
#

@before_invoke_hook(priority=10000)
async def database_connect(cog, ctx):
    """Before-hook to establish database connection"""
    logger.debug("Connected to database")
    ctx.db_session = ctx.bot.DBSession()


@after_invoke_hook(priority=10000)
async def database_cleanup(cog, ctx):
    """After-hook to cleanup after database connection"""
    logger.debug("Commiting database changes")
    ctx.db_session.commit()
    logger.debug("Commited database changes")

@before_invoke_hook(priority=1000)
async def attach_user(cog, ctx):
    """Before-hook to attach message author to ctx.db_user"""
    logger.debug("Getting user from database")
    ctx.db_user = await get_user(ctx.db_session, ctx.author.id)

#
#   Useful helper methods
#

async def get_user(session, discord_id):
    user = session.query(User).filter_by(discord_id=discord_id).first()

    if user is None:
        user = User(discord_id=discord_id)
        session.add(user)

    return user