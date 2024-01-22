from sqlalchemy.orm import sessionmaker
from aiogram import Dispatcher

from src.database.Tables.User import User


async def register_new_user(user_id: int, user_name: str, session_maker: sessionmaker) -> str:
    async with session_maker() as session:
        async with session.begin():
            new_user = User(
                user_id=user_id,
                user_name=user_name
            )
            session.add(new_user)
    
