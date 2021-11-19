from models.user import User

import logging

from utils.hooks import before_invoke_hook, after_invoke_hook
logger = logging.getLogger(__name__)

#
#   Custom Hooks 
#

def database_connect(func):
    priority = 10000

    def before_hook(cog, ctx):
        logger.debug("Connected to database")
        ctx.db_session = ctx.bot.DBSession()

    def after_hook(cog, ctx):
        logger.debug("Commiting database changes")
        ctx.db_session.commit()
        logger.debug("Commited database changes")
        
    if not hasattr(func, '__after_invokes') or func.__after_invokes is None:
        func.__after_invokes = []
    if not hasattr(func, '__before_invokes') or func.__before_invokes is None:
        func.__before_invokes = []

    func.__after_invokes.append((priority, after_hook))
    func.__before_invokes.append((priority, before_hook))

    return multi_hook(func)


@before_invoke_hook(priority=1000)
async def attach_database_user(cog, ctx):
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