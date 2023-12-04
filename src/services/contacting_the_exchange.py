import requests

from ..config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()


# Функция совершающая обмен курса
def exenge_rate():
    # URL API Fixer.io (Конечная точка последних ставок)
    url = 'http://data.fixer.io/api/latest'

    # Параметры запроса
    params = {
        'access_key': config.ch_api.access_key,
        # 'base': 'RUB',  # Базовая валюта для конвертации
        # 'symbols': 'GBP,JPY,EUR',  # Выходные валы
    }

    try:
        # Выполнение GET-запроса
        response = requests.get(url, params=params)

        # Проверка успешности запроса (200 OK)
        if response.status_code == 200:
            # Распечатка JSON-ответа
            return response.json()
        else:
            # Вывод ошибки, если запрос не был успешен
            return print('Ошибка 400')
    except requests.exceptions.RequestException as e:
        # Обработка ошибок связанных с сетью или запросом
        return print(f"Error: {e}")
