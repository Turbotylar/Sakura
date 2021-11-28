from sakura.models.base import Base
from sqlalchemy import Column, BigInteger, Integer, String, Boolean


class Guild(Base):
    __tablename__ = 'guilds'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger)

    is_debug_guild = Column(Boolean, default=False)

    # Role sets
    jail_role = Column(BigInteger, nullable=True)
    mute_role = Column(BigInteger, nullable=True)
    mod_role = Column(BigInteger, nullable=True)
    welcome_channel = Column(BigInteger, nullable=True)
    verified_role = Column(BigInteger, nullable=True)

    custom_prefix = Column(String(16), nullable=True)


    def __repr__(self) -> str:
        return f"<Guild({self.id=}, {self.discord_id=}, {self.custom_prefix=}>"
