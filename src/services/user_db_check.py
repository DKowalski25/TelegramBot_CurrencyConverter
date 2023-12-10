from ..database.redis import r


async def check_user_in_db(user_id: int) -> bool:
    key = user_id
    return r.exists(key)
