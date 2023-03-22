from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.database.models.bet_models.bet_model import Bet


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, unique=True)

    email = Column(String, nullable=False, unique=True)

    password = Column(String)

    bets: List[Bet] = relationship(
        "Bet",
        cascade="all, delete-orphan", lazy='joined'
    )
