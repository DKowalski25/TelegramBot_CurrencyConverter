from dataclasses import dataclass

from environs import Env

env = Env()


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм боту


@dataclass
class ChApi:
    access_key: str  # Ключ API


@dataclass
class Config:
    tg_bot: TgBot
    ch_api: ChApi


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        ch_api=ChApi(access_key=env('СHANGER_API_KEY'))
    )
