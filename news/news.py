import asyncio
import os

from chatgpt import ask_chatgpt
from GoogleNewsScraper import GoogleNewsScraper
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

GOOGLE_NEWS_TYPE_COMMON = "World News"
GOOGLE_NEWS_TYPE_TECH = "Tech & Innovation"
GOOGLE_NEWS_TYPE_BUSINESS = "Business & Finance"
GOOGLE_NEWS_TYPE_SCIENCE = "Science & Discovery"
GOOGLE_NEWS_TYPE_HEALTH = "Health & Wellness"
GOOGLE_NEWS_TYPE_SPORTS = "Sports"
GOOGLE_NEWS_TYPE_POLITICS = "Politics & Government"
GOOGLE_NEWS_TYPE_ENVIRONMENT = "Environment & Sustainability"
GOOGLE_NEWS_TYPE_ENTERTAINMENT = "Entertainment & Culture"
GOOGLE_NEWS_TYPE_FOOD = "Food & Lifestyle"
GOOGLE_NEWS_TYPE_ART = "Art & Fashion"

CHAT_GPT_PROMPT_DIGEST_160 = """Please make a digest of this news,
 strictly no more than 160 characters in English, for sending an SMS digest."""

CHAT_GPT_PROMPT_160 = """Please, make it under 160 symbols. That is required."""


async def news_scraper(search_text: str):
    log_pid = f"news-{os.getpid()}: "

    news = None
    selenium_driver = None
    try:
        proxy_url = None
        selenium_driver = await selenium_connect(proxy_url=proxy_url)
        news = GoogleNewsScraper(selenium_driver).scrape_by_search(search_text)
        await selenium_disconnect(selenium_driver)
        selenium_driver = None
        # send to chatgpt
        d(3)
        messages = [
            {
                "role": "user",
                "content": f"This is a text of one news: {news.get_news_text()[1:2000]}",
            },
            {
                "role": "user",
                "content": CHAT_GPT_PROMPT_DIGEST_160,
            },
        ]
        d(4)
        answer = await ask_chatgpt(messages)
        d(5)
        log.info(log_pid + "chatGPT: " + f" {answer}")

    except Exception as exception:
        log.error(log_pid + f"{exception}")
    finally:
        await selenium_disconnect(selenium_driver)


if __name__ == "__main__":
    # for news_type in GOOGLE_NEWS_TYPES.keys():
    asyncio.run(news_scraper(GOOGLE_NEWS_TYPE_TECH))
