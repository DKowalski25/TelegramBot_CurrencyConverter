from typing import Union

from src.utils import config

from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

postgres_url = URL.create(
        "postgresql+asyncpg",
        username=config.USERNAME_DB,
        host=config.HOST_DB,
        password=config.PASSWORD_DB,
        database=config.DATABASE_NAME,
        port=int(config.PORT_DB)
    )


def create_engine(url: Union[URL, str]) -> AsyncEngine:
    """The function creates an engin."""
    return create_async_engine(
        url=url,
        echo=True,
        pool_pre_ping=True
    )


@DeprecationWarning
async def proceed_schemas(engin: AsyncEngine, metadata: MetaData) -> None:
    """The function creates schemas in Date Base."""
    # async with engin.begin() as conn:
    #     await conn.run_sync(metadata.create_all)
    ...


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    """The function creates a sessionmaker."""
    return sessionmaker(engine, class_=AsyncSession)



