from collections import defaultdict

from aiogram.fsm.storage.redis import RedisStorage, Redis

r = Redis(host='localhost', port=6379, decode_responses=True)

storage = RedisStorage(redis=r)


# Создаем "базу данных" пользователей
user_answer = defaultdict(lambda: defaultdict(dict))
user_answer: dict[int, dict[int, dict[str, int | float | str]]]