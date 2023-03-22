from sqlalchemy import Column, String, ForeignKey, Integer

from src.database.config import Base


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    event_id = Column(String)

    user_id = Column(String, ForeignKey("users.uid"))

    amount = Column(String, nullable=False)

    status = Column(String)
