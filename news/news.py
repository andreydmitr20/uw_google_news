from config import config
from news.log import log, d
from old.GoogleNewsScraper import (
    GoogleNewsScraper,
    GOOGLE_NEWS_TYPES,
    GOOGLE_NEWS_TYPE_COMMON,
)


CHAT_GPT_PROMPT_DIGEST_160 = """Hello, please make a digest of this news,
 strictly no more than 160 characters in English, for sending an SMS digest."""

CHAT_GPT_PROMPT_160 = """Please, make it under 160 symbols. That is required."""

if __name__ == "__main__":
    news_type = GOOGLE_NEWS_TYPE_COMMON
    # for news_type in GOOGLE_NEWS_TYPES.keys():
    # news = GoogleNewsScraper(news_type).scrape()
    news = GoogleNewsScraper(news_type).scrape_by_search(news_type)
    log.info(news)
