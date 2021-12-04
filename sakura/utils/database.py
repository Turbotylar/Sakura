from sakura.models.guild import Guild
from sakura.models.user import User

import logging
logger = logging.getLogger(__name__)

    
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