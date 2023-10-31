import asyncio
import os
from datetime import datetime, timezone, timedelta

from config import config
from mylib.log import d, log, current_utc_date_int
from mylib.test_services import (
    SERVICE_POSTGRESQL,
    SERVICE_RABBITMQ,
    SERVICE_REDIS,
    SERVICE_SELENIUM,
    test_services,
)
import time

# plus time zone
UTC_TIMEDELTA_HOURS = 1

SCHEDULER_FOR_INTERESTS = [
    [0, "start"][1000, "w"],
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

NEWS_TYPE = {
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


def get_utc_now():
    return datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
        hours=UTC_TIMEDELTA_HOURS
    )


def is_between_by_scheduler_index(index: int, hour_minute_int: int) -> bool:
    if SCHEDULER_FOR_INTERESTS[index][0] <= hour_minute_int:
        if SCHEDULER_FOR_INTERESTS[index][1] == "stop":
            return True
        return hour_minute_int < SCHEDULER_FOR_INTERESTS[index + 1][0]
    return False


async def sender():
    log_pid = f"sender-{os.getpid()}: "
    await test_services(
        [
            # SERVICE_REDIS,
            # SERVICE_POSTGRESQL,
            SERVICE_SELENIUM,
            config.api_path + "check/",
        ],
        log_pid,
    )

    log.info(log_pid + "started")

    utc_now = get_utc_now()
    utc_date = utc_now.date()
    hour = utc_now.hour
    minute = utc_now.minute
    hour_minute_int = hour * 100 + minute
    # skip tasks before current time
    for scheduler_interests_index in range(len(SCHEDULER_FOR_INTERESTS)):
        if is_between_by_scheduler_index(scheduler_interests_index, hour_minute_int):
            break

    # main day loop for scheduler_interests_index
    while True:
        news_type = SCHEDULER_FOR_INTERESTS[scheduler_interests_index][1]
        if news_type == "start" or news_type == "stop":
            # wait
            log.info(log_pid + "waiting")
            while is_between_by_scheduler_index(
                scheduler_interests_index, hour_minute_int
            ):
                time.sleep(60)
                utc_now = get_utc_now()
                hour = utc_now.hour
                minute = utc_now.minute
                hour_minute_int = hour * 100 + minute
            if news_type == "start":
                scheduler_interests_index += 1
            else:
                scheduler_interests_index = 0
                continue

        # do task
        news_type = SCHEDULER_FOR_INTERESTS[scheduler_interests_index][1]
        log.info(log_pid + f"start task for interest '{NEWS_TYPE[news_type]}'")

        # TODO got list clients to whom we will send sms
        day_of_week = utc_now.weekday() + 1
        clients_list = [{"phone": "12345"}]
        clients_list_length = len(clients_list)
        log.info(
            log_pid
            + f"got {clients_list_length} clients for interest '{news_type}' and day of week {day_of_week}"
        )
        if clients_list_length != 0:
            # TODO get sms_text for interest and day_off_week
            sms_text = "test"
            log.info(log_pid + f"got sms text: '{sms_text}'")

            for client in clients_list:
                log.info(log_pid + f"send sms to client: {client}")
                # TODO send sms_text for client

        # next task
        scheduler_interests_index += 1
        # wait for beginning of new period if we should
        utc_now = get_utc_now()
        hour = utc_now.hour
        minute = utc_now.minute
        hour_minute_int = hour * 100 + minute
        if hour_minute_int < SCHEDULER_FOR_INTERESTS[scheduler_interests_index][0]:
            while not is_between_by_scheduler_index(
                scheduler_interests_index, hour_minute_int
            ):
                time.sleep(60)
                utc_now = get_utc_now()
                hour = utc_now.hour
                minute = utc_now.minute
                hour_minute_int = hour * 100 + minute


if __name__ == "__main__":
    asyncio.run(sender())
