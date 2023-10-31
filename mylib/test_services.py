import asyncio
import aiohttp

import os
from .api_lib import api_delete, api_get, api_post, api_put

from .redis_lib import redis_connect, redis_disconnect

# from .db_lib import db_connect, db_disconnect
from .selenium_lib import selenium_connect, selenium_disconnect
from .log import log, d
from .config import config

SERVICE_POSTGRESQL = "Postgresql"
SERVICE_RABBITMQ = "RabbitMQ"
SERVICE_REDIS = "Redis"
SERVICE_SELENIUM = "Selenium"


def log_service_is_not_ready(service: str, log_pid: str):
    log.warning(log_pid + f"test_services: " + service + " is not ready")


# async def test_posgresql(service: str, log_pid: str):
#     database = None
#     try:
#         database = await db_connect()
#         if database is None:
#             log_service_is_not_ready(service, log_pid)
#             return False
#     except Exception as exception:
#         log_service_is_not_ready(service, log_pid)
#         return False
#     finally:
#         await db_disconnect(database)
#     return True


async def test_selenium(service: str, log_pid: str):
    driver = None
    try:
        driver = await selenium_connect()
        if driver is None:
            log_service_is_not_ready(service, log_pid)
            return False
    except Exception as exception:
        log_service_is_not_ready(service, log_pid)
        return False
    finally:
        await selenium_disconnect(driver)
    return True


# async def test_rabbitmq(service: str,log_pid:str):
#     try:
#         connection_listener_parser = await connect_to_broker()
#         async with connection_listener_parser:
#             channel_listener_parser = await connection_listener_parser.channel()
#             if channel_listener_parser is None:
#                 log_service_is_not_ready(service,log_pid)
#                 return False

#     except Exception as exception:
#         log_service_is_not_ready(service,log_pid)
#         # save_to_server_log(f"{exception}")
#         return False
#     return True


async def test_redis(service: str, log_pid: str):
    redis_connection = None
    try:
        redis_connection = await redis_connect()
        answer = await redis_connection.ping()
    except Exception as exception:
        log_service_is_not_ready(service, log_pid)
        # save_to_server_log(f"{exception}")
        return False
    finally:
        await redis_disconnect(redis_connection)
    return True


async def test_api(service: str, log_pid: str):
    response = None
    try:
        response = await api_get(url=service)
        # print(f"{response}")
        if response and type(response) == list and response[0]["api_status"] == "ok":
            return True
    except Exception as exception:
        log_service_is_not_ready(service, log_pid)
        # print(f"{exception}")
    return False


async def test_services(services_list: list, log_pid: str = ""):
    if services_list:
        for service in services_list:
            if service.find("http") == 0:
                # api
                while not await test_api(service, log_pid):
                    await asyncio.sleep(2)
            # elif service == SERVICE_POSTGRESQL:
            #     while not await test_posgresql(service, log_pid):
            #         await asyncio.sleep(2)

            # elif service == SERVICE_RABBITMQ:
            #     while not await test_rabbitmq(service,log_pid):
            #         await asyncio.sleep(2)

            elif service == SERVICE_REDIS:
                while not await test_redis(service, log_pid):
                    await asyncio.sleep(2)

            elif service == SERVICE_SELENIUM:
                while not await test_selenium(service, log_pid):
                    await asyncio.sleep(2)

            else:
                log_service_is_not_ready(service, log_pid)
