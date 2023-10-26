import os
import asyncio

from GoogleNewsScraper import (
    GOOGLE_NEWS_TYPE_COMMON,
    GOOGLE_NEWS_TYPES,
    GoogleNewsScraper,
)
from mylib.log import d, log
from mylib.selenium_lib import selenium_connect, selenium_disconnect
from mylib.test_services import (
    SERVICE_POSTGRESQL,
    SERVICE_RABBITMQ,
    SERVICE_REDIS,
    SERVICE_SELENIUM,
    test_services,
)

from config import config

CHAT_GPT_PROMPT_DIGEST_160 = """Hello, please make a digest of this news,
 strictly no more than 160 characters in English, for sending an SMS digest."""

CHAT_GPT_PROMPT_160 = """Please, make it under 160 symbols. That is required."""


async def news_scraper():
    log_pid = f"news-{os.getpid()}: "
    selenium_driver = None
    try:
        proxy_url = None
        selenium_driver = await selenium_connect(proxy_url=proxy_url)
        news_type = GOOGLE_NEWS_TYPE_COMMON
        # for news_type in GOOGLE_NEWS_TYPES.keys():
        # news = GoogleNewsScraper(news_type).scrape()
        news = GoogleNewsScraper(selenium_driver).scrape_by_search(news_type)
        log.info(log_pid + f"{news}")
    except Exception as exception:
        log.error(log_pid + f"{exception}")
    finally:
        await selenium_disconnect(selenium_driver)


if __name__ == "__main__":
    asyncio.run(news_scraper())
