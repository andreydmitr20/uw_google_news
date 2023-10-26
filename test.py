from config import config
from log import log, d
from GoogleNewsScraper import (
    GoogleNewsScraper,
    GOOGLE_NEWS_TYPES,
    GOOGLE_NEWS_TYPE_COMMON,
)

if __name__ == "__main__":
    news_type = GOOGLE_NEWS_TYPE_COMMON
    # for news_type in GOOGLE_NEWS_TYPES.keys():
    news = GoogleNewsScraper(news_type).scrape()
    log.info(news)
