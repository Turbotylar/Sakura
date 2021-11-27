from sakura.models.base import Base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger)
    is_bot_dev = Column(Boolean, default=False)
    location = Column(String(128), nullable=True)


    def __repr__(self) -> str:
        return f"<User({self.id=}, {self.discord_id=}, {self.is_bot_dev=})>"