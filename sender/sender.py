import asyncio
import os
import time
from datetime import datetime, timedelta, timezone

from mylib.api_lib import api_delete, api_get, api_post, api_put
from mylib.log import current_utc_date_int, d, log
from mylib.test_services import (
    SERVICE_POSTGRESQL,
    SERVICE_RABBITMQ,
    SERVICE_REDIS,
    SERVICE_SELENIUM,
    test_services,
)
from mylib.twilio_lib import MESSAGE_SID_LENGTH, send_sms

from config import config

SCHEDULER_FOR_INTERESTS = [
    [0, "start"],
    [1000, "w"],
    [1030, "t"],
    [1100, "b"],
    [1130, "s"],
    [1200, "h"],
    [1230, "p"],
    [1300, "o"],
    [1330, "e"],
    [1400, "n"],
    [1430, "f"],
    [1500, "a"],
    [1530, "stop"],
]

NEWS_SEARCH_TEXT = {
    "w": "Today top world news",
    "t": "Today tech and innovations top news",
    "b": "Today business and finance top news",
    "s": "Today science and discovery top news",
    "h": "Today health and wellness top news",
    "p": "Today sport top news",
    "o": "Today politics and government top news",
    "e": "Today environment and sustainability top news",
    "n": "Today entertainment and culture top news",
    "f": "Today food and lifestyle top news",
    "a": "Today art and fashion top news",
}


def get_news_search_text(interest: str) -> str:
    try:
        return NEWS_SEARCH_TEXT[interest]
    except:
        return NEWS_SEARCH_TEXT["w"]


GET_CLIENTS_LIST_ATTEMPTS_MAX = 5
GET_SMS_TEXT_ATTEMPTS_MAX = 5
SEND_SMS_ATTEMPTS_MAX = 5
GET_TOKEN_ATTEMPTS_MAX = 5
WAIT_SECONDS_AFTER_ERROR = 5


# production only
# def get_utc_now():
#     return datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
#         hours=int(config.timezone)
#     )


# SLEEP_TIME_IN_SECONDS = 60

# debug only
SLEEP_TIME_IN_SECONDS = 1
UTC_NOW = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
    hours=int(config.timezone)
)


def get_utc_now():
    global UTC_NOW
    UTC_NOW = UTC_NOW + timedelta(minutes=10)
    log.info(f"{get_hour_minute_int(UTC_NOW)}")
    return UTC_NOW


def get_hour_minute_int(utc_now):
    hour = utc_now.hour
    minute = utc_now.minute
    return hour * 100 + minute


def is_between_by_scheduler_index(index: int, hour_minute_int: int) -> bool:
    if SCHEDULER_FOR_INTERESTS[index][0] <= hour_minute_int:
        if SCHEDULER_FOR_INTERESTS[index][1] == "stop":
            return True
        return hour_minute_int < SCHEDULER_FOR_INTERESTS[index + 1][0]
    return False


async def get_clients_list(
    interest: str, weekday: int, token: str, log_pid: str
) -> list:
    """get_clients_list"""
    # select * from news_clients
    # where (days_in_week =1 or days_in_week =2) and news_type like '%w%'
    log_pid += "get_clients_list: "
    attempt = 0
    while attempt < GET_CLIENTS_LIST_ATTEMPTS_MAX:
        attempt += 1

        try:
            # get sms_text
            api_url = (
                config.news_api_path + f"news/api/client/list/sms/{weekday}/{interest}/"
            )
            data = await api_get(
                api_url,
                token=token,
            )
            # log.info(log_pid + f"{data}")
            if not (isinstance(data, list)):
                raise Exception(f"Can not get clients list for {api_url}")

            return data

        except Exception as exception:
            log.warning(log_pid + f"{exception}")
            time.sleep(WAIT_SECONDS_AFTER_ERROR)
    log.error(log_pid + f"can not get clients list")
    return []


async def get_sms_text(search_text: str, token: str, log_pid: str) -> str:
    log_pid += "get_sms_text: "
    attempt = 0
    while attempt < GET_SMS_TEXT_ATTEMPTS_MAX:
        attempt += 1

        try:
            # get sms_text
            api_url = config.news_api_path + f"news/api/scrape/"
            data = await api_get(
                api_url,
                params={
                    "search": search_text,
                },
                token=token,
            )
            if not (
                isinstance(data, list) and len(data) >= 1 and isinstance(data[0], dict)
            ):
                raise Exception(f"Can not get sms text for {api_url}")
            result = data[0]
            if result["sms_text"] != "":
                return result["sms_text"]
            if result["error"] != "":
                raise Exception(result["error"])
            raise Exception("get empty sms text")

        except Exception as exception:
            log.warning(log_pid + f"{exception}")
            time.sleep(WAIT_SECONDS_AFTER_ERROR)

    log.error(log_pid + f"can not get sms text")
    return ""


async def send_sms_to_client(sms_text: str, client: dict, log_pid: str):
    """send_sms"""
    log_pid += "send_sms: "
    attempt = 0
    while attempt < SEND_SMS_ATTEMPTS_MAX:
        attempt += 1

        try:
            if config.send_sms != "False":
                sid = send_sms(
                    sms_text=sms_text,
                    from_phone=config.from_phone,
                    to_phone=client["phone"],
                )
                if len(sid) != MESSAGE_SID_LENGTH:
                    raise Exception("No good sms message sid returned")

            return

        except Exception as exception:
            log.warning(log_pid + f"{exception}")
            time.sleep(WAIT_SECONDS_AFTER_ERROR)
    log.error(log_pid + f"can not send sms")
    return


async def get_token(log_pid: str) -> str:
    """get access token"""
    log_pid += "get_token: "
    attempt = 0
    while attempt < GET_TOKEN_ATTEMPTS_MAX:
        attempt += 1
        try:
            api_url = config.news_api_path + f"api/token/"
            jwt = await api_post(
                api_url,
                data={
                    "username": config.news_api_user,
                    "password": config.news_api_pass,
                },
            )
            if not (isinstance(jwt, dict) and "access" in jwt.keys()):
                raise Exception(f"Can not get access token for {api_url}")
            # log.info(log_pid + f"{jwt}")
            return jwt["access"]
        except Exception as exception:
            log.warning(log_pid + f"{exception}")
            time.sleep(WAIT_SECONDS_AFTER_ERROR)
    log.error(log_pid + f"can not get auth token")
    return ""


async def sender():
    log_pid = f"sender-{os.getpid()}: "
    await test_services(
        [
            # SERVICE_REDIS,
            # SERVICE_POSTGRESQL,
            SERVICE_SELENIUM,
            config.news_api_path + "news/api/check/",
        ],
        log_pid,
    )

    log.info(log_pid + "started")

    utc_now = get_utc_now()
    hour_minute_int = get_hour_minute_int(utc_now)
    # skip tasks before current time
    for scheduler_interests_index in range(len(SCHEDULER_FOR_INTERESTS)):
        if is_between_by_scheduler_index(scheduler_interests_index, hour_minute_int):
            break

    # main day loop for scheduler_interests_index
    while True:
        interest = SCHEDULER_FOR_INTERESTS[scheduler_interests_index][1]
        if interest == "start" or interest == "stop":
            # wait
            log.info(log_pid + "waiting")
            while is_between_by_scheduler_index(
                scheduler_interests_index, hour_minute_int
            ):
                time.sleep(SLEEP_TIME_IN_SECONDS)
                utc_now = get_utc_now()
                hour_minute_int = get_hour_minute_int(utc_now)

            if interest == "start":
                scheduler_interests_index += 1
            else:
                scheduler_interests_index = 0
                continue

        # do task
        interest = SCHEDULER_FOR_INTERESTS[scheduler_interests_index][1]
        log.info(
            log_pid + f"start task for interest '{get_news_search_text(interest)}'"
        )

        # got token
        token = await get_token(log_pid)
        if token != "":
            # got list clients to whom we will send sms
            weekday = utc_now.weekday() + 1
            clients_list = await get_clients_list(interest, weekday, token, log_pid)
            clients_list_length = len(clients_list)
            log.info(
                log_pid
                + f"got {clients_list_length} clients for interest '{interest}' and day of week {weekday}"
            )
            if clients_list_length != 0:
                #  get sms_text for interest and day_off_week
                sms_text = await get_sms_text(
                    get_news_search_text(interest), token, log_pid
                )
                if sms_text != "":
                    log.info(log_pid + f"got sms text: '{sms_text}'")

                    for client in clients_list:
                        log.info(log_pid + f"send sms to client: {client}")
                        # send sms_text for client
                        await send_sms_to_client(sms_text, client, log_pid)

        # next task
        scheduler_interests_index += 1
        # wait for beginning of new period if we should
        utc_now = get_utc_now()
        hour_minute_int = get_hour_minute_int(utc_now)

        if hour_minute_int < SCHEDULER_FOR_INTERESTS[scheduler_interests_index][0]:
            while not is_between_by_scheduler_index(
                scheduler_interests_index, hour_minute_int
            ):
                time.sleep(SLEEP_TIME_IN_SECONDS)
                utc_now = get_utc_now()
                hour_minute_int = get_hour_minute_int(utc_now)


if __name__ == "__main__":
    asyncio.run(sender())
