import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import BaseModel

# from src.database.Tables.exchange_history import ExchangeHistory


class User(BaseModel):
    """User table."""
    __tablename__ = 'users'

    # Telegram user id
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False, primary_key=True)
    # Telegram user name
    user_name: Mapped[str] = mapped_column(nullable=False)
    # Registration date
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.date.today())
    # Last update date
    upd_date: Mapped[datetime.datetime] = mapped_column(DATE, onupdate=datetime.date.today())
    #
    exchange_histories: Mapped[list['ExchangeHistory']] = relationship(back_populates='users', uselist=True)

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'


class ExchangeHistory(BaseModel):
    """Exchange history model."""
    __tablename__ = 'exchange_histories'

    exchange_id: Mapped[int] = mapped_column(autoincrement=True, unique=True, nullable=False, primary_key=True)
    count_currency1: Mapped[float]
    currency_1: Mapped[str] = mapped_column(nullable=False)
    exchange_amount: Mapped[float] = mapped_column(nullable=False)
    currency_2: Mapped[str] = mapped_column(nullable=False)
    users: Mapped['User'] = relationship(back_populates='exchange_histories', uselist=False)
    user_id_fk: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    def __str__(self) -> str:
        return f"ID: {self.exchange_id}, Amount: {self.exchange_amount}," \
               f" Currency 1: {self.currency_1}, Currency 2: {self.currency_2}"
