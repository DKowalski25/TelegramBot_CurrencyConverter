import aiohttp
import asyncio

from src.config_data.config import Config, load_config

config: Config = load_config()

async def exenge_rate_random():
    """ Функция получения пары 1 EUR: что то рандомное"""
    url = 'http://data.fixer.io/api/latest'

    params = {
        'access_key': config.ch_api.access_key,
        # 'base': 'RUB',  # Базовая валюта для конвертации
        # 'symbols': 'GBP,JPY,EUR',  # Выходные валы
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    json_data = await response.json()
                    inner_dict = json_data.get("rates")

                    return inner_dict
                else:
                    return print(f'Ошибка {response.status}')
    except aiohttp.ClientError as e:
        return print(f"Error: {e}")


