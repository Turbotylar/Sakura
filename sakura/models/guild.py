from sakura.models.base import Base
from sqlalchemy import Column, BigInteger, Integer, String, Boolean


class Guild(Base):
    __tablename__ = 'guilds'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger)

    # Role sets
    jail_role = Column(BigInteger, nullable=True)
    mute_role = Column(BigInteger, nullable=True)
    mod_role = Column(BigInteger, nullable=True)

    custom_prefix = Column(String, nullable=True)


    def __repr__(self) -> str:
        return f"<Guild({self.id=}, {self.discord_id=}, {self.custom_prefix=}>"