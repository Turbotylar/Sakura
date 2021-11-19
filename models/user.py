from models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, text

class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    is_bot_dev = Column(Boolean, default=False)


    def __repr__(self) -> str:
        return f"<User(id={self.id}, discord_id={self.discord_id}, is_bot_dev={self.is_bot_dev})>"