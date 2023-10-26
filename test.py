from config import config
from log import log
from GoogleNewsScraper import GoogleNewsScraper, GOOGLE_NEWS_TYPES

if __name__ == "__main__":
    news = GoogleNewsScraper().scrape()
    log.info(f"{news}")
