import asyncio
import os

from config import config
from mylib.log import d, log
from mylib.test_services import (
    SERVICE_POSTGRESQL,
    SERVICE_RABBITMQ,
    SERVICE_REDIS,
    SERVICE_SELENIUM,
    test_services,
)


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


if __name__ == "__main__":
    asyncio.run(sender())
