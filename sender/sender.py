from mylib.log import log, d
import os
import asyncio


async def sender():
    log_pid = f"sender-{os.getpid()}: "
    log.info(log_pid + "started")


if __name__ == "__main__":
    asyncio.run(sender())
