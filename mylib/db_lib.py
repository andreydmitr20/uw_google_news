import asyncio
from databases import Database

from .config import config
from .log import log, d

# Start a transaction
# async with database.transaction():
#     query = """DELETE FROM GfgExample"""
#     await database.execute(query=query)


async def db_connect():
    db_dsn = (
        config.db_proto
        + config.db_user
        + ":"
        + config.db_pass
        + "@"
        + config.db_host
        + ":"
        + config.db_port
        + "/"
        + config.db_name
    )
    database = None
    try:
        database = Database(db_dsn)

        await database.connect()
        return database

    except Exception as exception:
        log.warning(f"{exception}")
        return None


async def db_disconnect(database):
    if database:
        await database.disconnect()


# query = """INSERT INTO T(id,name) VALUES (:id ,:name)"""
# values =     {"id":1,"name": "abc"}
async def db_execute(database, query: str, values: dict = {}) -> bool:
    try:
        await database.execute(query=query, values=values)
        return True
    except Exception as exception:
        log.warning(f"db_lib: db_execute: {query}. {exception}")
        return False


# rows = await db_fetch_all(
#     db,
#     'select count(*) as "count_running_tasks" from google_maps_tasks where is_running = True',
# )
# row = rows[0]
# print(row["count_running_tasks"])
async def db_fetch_all(database, query: str, values: dict = {}) -> list:
    try:
        rows = await database.fetch_all(query=query, values=values)
        return rows
    except Exception as exception:
        log.warning(f"db_lib: db_fetch_all: {query}. {exception}")
        return None
