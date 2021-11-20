from sakura.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean

class Guild(Base):
    __tablename__ = 'guilds'


    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)

    # Role sets
    jail_role = Column(Integer, nullable=True)
    mute_role = Column(Integer, nullable=True)
    mod_role = Column(Integer, nullable=True)

    custom_prefix = Column(String, nullable=True)

    


    def __repr__(self) -> str:
        return f"<Guild(id={self.id}, discord_id={self.discord_id}, custom_prefix={self.custom_prefix}>"
