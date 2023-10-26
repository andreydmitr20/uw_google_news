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

GOOGLE_NEWS_TYPE_WORLD = "World News"
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

GOOGLE_NEWS_TYPE = [
    GOOGLE_NEWS_TYPE_WORLD,
    GOOGLE_NEWS_TYPE_TECH,
    GOOGLE_NEWS_TYPE_BUSINESS,
    GOOGLE_NEWS_TYPE_SCIENCE,
    GOOGLE_NEWS_TYPE_HEALTH,
    GOOGLE_NEWS_TYPE_SPORTS,
    GOOGLE_NEWS_TYPE_POLITICS,
    GOOGLE_NEWS_TYPE_ENVIRONMENT,
    GOOGLE_NEWS_TYPE_ENTERTAINMENT,
    GOOGLE_NEWS_TYPE_FOOD,
    GOOGLE_NEWS_TYPE_ART,
]


SMS_STOP_KEYPHRASE_LIST = [
    "sex",
    "(160 characters)",
    "News not available in your country",
]
MAX_SMS_LENGTH_IN_CHARS = 160


async def news_scraper(result: dict):
    log_pid = f"news-{os.getpid()}: "

    search_text = result["search_text"]
    sms_text = ""

    selenium_driver = None
    try:
        attempt = 0
        while attempt < 5:
            attempt += 1

            sms_text = ""
            log.info(
                log_pid + f"Attempt: {attempt} getting news for >>>'{search_text}'."
            )
            try:
                proxy_url = None
                selenium_driver = await selenium_connect(proxy_url=proxy_url)
                news = GoogleNewsScraper(selenium_driver).scrape_by_search(
                    search_text, attempt
                )

                await selenium_disconnect(selenium_driver)
                selenium_driver = None

                # send to chatgpt
                log.info(log_pid + "chatGPT: has started")

                messages = [
                    {
                        "role": "user",
                        "content": f"This is a text of one news: {news.get_news_text()[1:2000]}",
                    },
                    {
                        "role": "user",
                        "content": f"""Please make a digest of this news,
                        strictly no more than {MAX_SMS_LENGTH_IN_CHARS} 
                        characters in English, without internet links.""",
                    },
                ]
                answer = await ask_chatgpt(messages)
                # log.info(log_pid + "chatGPT: " + f" {answer}")
                sms_text = answer["answer"]["content"]
                log.info(log_pid + f">>>{search_text}>>> SMS:{sms_text}")

                # check sms
                d(1)
                if sms_text.strip() == "" or len(sms_text) > MAX_SMS_LENGTH_IN_CHARS:
                    continue
                is_stop_keyphrase_found = False
                d(2)
                for keyphrase in SMS_STOP_KEYPHRASE_LIST:
                    if sms_text.find(keyphrase) >= 0:
                        is_stop_keyphrase_found = True
                        break
                d(3)
                if is_stop_keyphrase_found:
                    continue
            except Exception as exception:
                log.error(log_pid + f"{exception}")
            break

    except Exception as exception:
        log.error(log_pid + f"{exception}")
    finally:
        await selenium_disconnect(selenium_driver)

    result["sms_text"] = sms_text


if __name__ == "__main__":
    for news_type in GOOGLE_NEWS_TYPE:
        result = {"search_text": news_type, "sms_text": ""}
        asyncio.run(news_scraper(result))
        log.info(f">>>{result['search_text']}>>> SMS:{result['sms_text']}")
