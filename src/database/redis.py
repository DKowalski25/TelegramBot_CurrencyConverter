from aiogram.fsm.storage.redis import RedisStorage, Redis

redis = Redis(host='localhost',
              port=6379,
              db=0,
              decode_responses=True)

storage = RedisStorage(redis=redis)

