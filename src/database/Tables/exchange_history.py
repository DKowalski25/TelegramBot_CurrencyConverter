import datetime

from sqlalchemy import ForeignKey

from src.database import BaseModel, User
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ExchangeHistory(BaseModel):
    """Exchange history model."""
    __tablename_ = 'exchange_histories'

    exchange_id: Mapped[int] = mapped_column(autoincrement=True, unique=True, nullable=False, primary_key=True)
    exchange_amount: Mapped[float | int] = mapped_column(nullable=False)
    currency_1: Mapped[str] = mapped_column(nullable=False)
    currency_2: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[User] = relationship(back_populates='exchange_histories', uselist=False)
    user_id_fk: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
