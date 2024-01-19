import os

from typing import Final
from dotenv import load_dotenv

from .exceptions.configurate_exceptions import EnvDependNotFound

load_dotenv()


def get_env_var(var_name: str) -> str:
    """
       :raise EnvDependNotFound if value in None
       :param var_name: Env var name
       :return: Var value by name
       """
    value: str | None = os.getenv(var_name)
    if value is None:
        raise EnvDependNotFound(var_name)
    else:
        return value


BOT_TOKEN: Final[str] = get_env_var("BOT_TOKEN")
CHANGER_API_KEY: Final[str] = get_env_var("CHANGER_API_KEY")
USERNAME_DB: Final[str] = get_env_var("USERNAME_DB")
HOST_DB: Final[str] = get_env_var("HOST_DB")
PASSWORD_DB: Final[str] = get_env_var("PASSWORD_DB")
DATABASE_NAME: Final[str] = get_env_var("DATABASE_NAME")
PORT_DB: Final[str] = get_env_var("PORT_DB")
