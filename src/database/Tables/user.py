import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import BaseModel, ExchangeHistory


class User(BaseModel):
    """User table."""
    __tablename__ = 'users'

    # Telegram user id
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False, primary_key=True)
    # Telegram user name
    user_name: Mapped[str] = mapped_column(nullable=False)
    # Registration date
    reg_date: Mapped[int] = mapped_column(DATE, default=datetime.date.today())
    # Last update date
    upd_date: Mapped[int] = mapped_column(DATE, onupdate=datetime.date.today())
    #
    exchange_histories: Mapped[list[ExchangeHistory]] = relationship(back_populates='user', uselist=True)


    def __str__(self) -> str:
        return f'<User:{self.user_id}>'

