from collections import defaultdict

from aiogram.fsm.storage.redis import RedisStorage, Redis

r = Redis(host='redis-17083.c302.asia-northeast1-1.gce.cloud.redislabs.com', port=17083, decode_responses=True)

storage = RedisStorage(redis=r)


# Создаем "базу данных" пользователей
user_answer = defaultdict(lambda: defaultdict(dict))
user_answer: dict[int, dict[int, dict[str, int | float | str]]]

