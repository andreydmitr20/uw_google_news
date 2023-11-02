import asyncio
import redis
from .config import config

# redis_connector: redis.Redis = redis.Redis(
#     host="localhost", port=6379, db=0, decode_responses=False
# )

# redis_connection = None
#     try:
#         redis_connection = await redis_connect()
#         await redis_set_by_hash_field(redis_connection, "1", "json", json.dumps({"test": "ok"}))
#         res = await redis_get_by_hash_field(redis_connection, "1", "json")
#         print(f"{res.decode()}")
#     finally:
#         await redis_disconnect(redis_connection)


async def redis_connect():
    try:
        connection = await redis.asyncio.Redis(
            host=config.redis_host, port=config.redis_port_int, decode_responses=False
        )
        return connection
    except Exception as exception:
        return None


async def redis_disconnect(connection):
    if connection:
        await connection.aclose()


async def redis_set_by_hash_field(redis_connection, hash: str, field: str, value: str):
    try:
        await redis_connection.hset(hash, field, value)
        return True
    except Exception as exception:
        return False


async def redis_get_by_hash_field(redis_connection, hash: str, field: str):
    try:
        return await redis_connection.hget(hash, field)
    except Exception as exception:
        return None
