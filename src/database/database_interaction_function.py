from sqlalchemy.orm import sessionmaker

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

