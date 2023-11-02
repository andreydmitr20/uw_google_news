import asyncio
import os

from .chatgpt import ask_chatgpt, is_chatgpt_error_rate_limit
from .GoogleNewsScraper import GoogleNewsScraper
from .mylib.log import d, log
from .mylib.selenium_lib import selenium_connect, selenium_disconnect
from .mylib.test_services import (
    SERVICE_POSTGRESQL,
    SERVICE_RABBITMQ,
    SERVICE_REDIS,
    SERVICE_SELENIUM,
    test_services,
)

from .config import config
from celery import shared_task

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
    # "sex".lower(),
    " characters)".lower(),
    "News not available in your country".lower(),
    "unavailable due to regional restrictions".lower(),
    "Content unavailable".lower(),
    "I can't generate the story".lower(),
    "Access Denied".lower(),
    "Website blocked".lower(),
]
MAX_SMS_LENGTH_IN_CHARS = 160
MAX_CHARS_IN_NEWS_TEXT = 3000


@shared_task
def news_scraper(search_text: str) -> dict:
    log_pid = f"news-{os.getpid()}: "

    result = {
        "search_text": search_text,
        "news_url": "",
        "sms_text": "",
        "error": "External error",
    }

    attempt = 0
    while attempt < 5:
        attempt += 1

        sms_text = ""
        log.info(log_pid + f"Attempt: {attempt} getting news for '{search_text}'.")
        # scrape news text
        selenium_driver = None
        try:
            proxy_url = None
            selenium_driver = asyncio.run(selenium_connect(proxy_url=proxy_url))
            news_scraper = GoogleNewsScraper(selenium_driver)

            asyncio.run(news_scraper.scrape_by_search(search_text, attempt))
        except Exception as exception:
            log.error(log_pid + f"{exception}")
        finally:
            asyncio.run(selenium_disconnect(selenium_driver))
        news_text = news_scraper.get_news_text()[0:MAX_CHARS_IN_NEWS_TEXT]
        if news_text.strip() == "":
            continue
        result["news_url"] = news_scraper.get_news_url()
        # send to chatgpt
        try:
            chatgpt_data = {
                "answer": "",
                "error": "",
                "messages": [
                    {
                        "role": "user",
                        "content": f"This is a text of one news: {news_text}",
                    },
                    {
                        "role": "user",
                        "content": f"""Please make a digest of this news,
                    strictly less or equal {MAX_SMS_LENGTH_IN_CHARS} 
                    characters in English, without internet links.""",
                    },
                    {
                        "role": "user",
                        "content": f"Make it under {MAX_SMS_LENGTH_IN_CHARS}. That is required. And without noting characters count.",
                    },
                ],
            }
            # chatgpt_data_result = ask_chatgpt(chatgpt_data)
            ask_chatgpt(chatgpt_data, log_pid)
            chatgpt_data_result = chatgpt_data
            # log.info(log_pid + "chatGPT: " + f" {chatgpt_data_result}")
            error = chatgpt_data_result["error"]
            if error != "":
                if is_chatgpt_error_rate_limit(error):
                    result["error"] = error
                    return result
                log.error(log_pid + "chatGPT: " + f"Error: {error}")
                continue
            sms_text = chatgpt_data_result["answer"]
            # log.info(log_pid + f">>>{search_text}>>>{sms_text}")

            # check sms
            if sms_text.strip() == "":
                log.info(log_pid + f" text is empty")
                continue
            if len(sms_text) > MAX_SMS_LENGTH_IN_CHARS:
                log.info(
                    log_pid
                    + f" text length is more than {MAX_SMS_LENGTH_IN_CHARS}: {sms_text}"
                )

                continue
            is_stop_keyphrase_found = False
            sms_text_lower = sms_text.lower()
            for keyphrase in SMS_STOP_KEYPHRASE_LIST:
                if sms_text_lower.find(keyphrase) >= 0:
                    is_stop_keyphrase_found = True
                    log.info(log_pid + f" stop phrase found '{keyphrase}: {sms_text}")
                    break
            if is_stop_keyphrase_found:
                continue
        except Exception as exception:
            log.error(log_pid + f"{exception}")

        result["error"] = ""
        break

    result["sms_text"] = sms_text
    return result
