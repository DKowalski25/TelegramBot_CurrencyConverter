from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from src.database.tables import User, ExchangeHistory


async def register_new_user(user_id: int, user_name: str, session_maker: sessionmaker):
    """The function registers user in the database."""

    async with session_maker() as session:
        async with session.begin():
            new_user = User(
                user_id=user_id,
                user_name=user_name
            )
            session.add(new_user)


async def add_exchange_history(count_cur1: float, exchange_amount: float, currency_1: str,
                               currency_2: str, user_id_fk: int, session_maker: sessionmaker):
    """The function adds data about the exchange to the database."""

    async with session_maker() as session:
        async with session.begin():
            new_history_entry = ExchangeHistory(
                count_currency1=count_cur1,
                exchange_amount=exchange_amount,
                currency_1=currency_1,
                currency_2=currency_2,
                user_id_fk=user_id_fk
            )
            session.add(new_history_entry)


async def get_exchange_history(user_id: int, session_maker: sessionmaker) -> list[ExchangeHistory]:
    """Get exchange history by user id."""

    async with session_maker() as session:
        history_entries = await session.execute(
                select(ExchangeHistory).join(User).filter(User.user_id == user_id)
            )
        return history_entries.scalars().all()


async def format_exchange_history(history_entries: list[ExchangeHistory]) -> str:
    """
    The function converts the dictionary received in "get_exchange_history"
    into a string representing the exchange history.
    """
    formatted_history = "История:\n"
    for entry in history_entries:
        formatted_entry = f"{entry.exchange_id}. {entry.count_currency1} {entry.currency_1} to {entry.currency_2}" \
                          f" - {entry.exchange_amount}"
        formatted_history += formatted_entry + "\n\n"
    return formatted_history
