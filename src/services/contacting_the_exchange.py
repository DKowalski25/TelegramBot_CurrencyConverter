import aiohttp

from ..utils import config


async def get_rate():
    """The function of getting EUR quotes."""

    url = 'http://data.fixer.io/api/latest'

    params = {
        'access_key': config.CHANGER_API_KEY,
        'base': 'EUR',  # The base currency for conversion
        # 'symbols': 'GBP,JPY,EUR',  # Output currencies
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


async def currency_relations(currency: str, name: str) -> float:
    """The function finds currency relations."""

    rates = await get_rate()
    rates_transformation = rates[name] / rates[currency]
    return rates_transformation


async def exchange_rate(amount: int, curr_1: str, curr_2: str):
    """The function receives the requested exchange rate."""

    right_pair = await currency_relations(curr_1, curr_2)
    result = (amount * right_pair)
    return result



