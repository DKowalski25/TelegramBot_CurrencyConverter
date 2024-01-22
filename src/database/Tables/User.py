import datetime

from aiogram import Dispatcher
from sqlalchemy import Column, Integer, String, VARCHAR, DATE
from sqlalchemy.orm import sessionmaker

from ..base import BaseModel, metadata


class User(BaseModel):
    """User table."""
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    # Telegram user name
    user_name = Column(VARCHAR(32), nullable=False)
    # Registration date
    reg_date = Column(DATE, default=datetime.date.today())
    # Last update date
    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'



# async def register_new_user(user_id: int, user_name: str, dp: Dispatcher) -> None:
#     session_maker = dp.storage['session_maker']
#     async with session_maker() as session:
#         async with session.begin():
#             new_user = User(
#                 user_id=user_id,
#                 user_name=user_name
#             )
#             session.add(new_user)
