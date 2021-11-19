from models.user import User

#
#   Before/After Invoke hooks
#

async def database_connect(ctx):
    """Before-hook to establish database connection"""
    ctx.db_session = ctx.bot.DBSession()

async def database_cleanup(ctx):
    """After-hook to cleanup after database connection"""
    ctx.db_session.commit()

async def attach_user(ctx):
    """Before-hook to attach message author to ctx.db_user"""
    ctx.db_user = get_user(ctx.db_session, ctx.author.id)

#
#   Useful helper methods
#

async def get_user(session, discord_id):
    user = session.query(User).filter_by(discord_id=discord_id).first()

    if user is None:
        user = User(discord_id=discord_id)
        session.add(user)

    return user