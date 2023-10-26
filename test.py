from config import config
from log import log, d
from GoogleNewsScraper import GoogleNewsScraper, GOOGLE_NEWS_TYPES

if __name__ == "__main__":
    d(1)
    for news_type in GOOGLE_NEWS_TYPES.keys():
        d(2)
        news = GoogleNewsScraper(news_type).scrape()
        log.info(news)
