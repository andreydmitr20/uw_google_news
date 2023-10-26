from log import log
import requests
from bs4 import *

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

GOOGLE_NEWS_TYPES = {
    GOOGLE_NEWS_TYPE_COMMON.lower(): "",
    GOOGLE_NEWS_TYPE_TECH.lower(): "",
    GOOGLE_NEWS_TYPE_BUSINESS.lower(): "",
    GOOGLE_NEWS_TYPE_SCIENCE.lower(): "",
    GOOGLE_NEWS_TYPE_HEALTH.lower(): "",
    GOOGLE_NEWS_TYPE_SPORTS.lower(): "",
    GOOGLE_NEWS_TYPE_POLITICS.lower(): "",
    GOOGLE_NEWS_TYPE_ENVIRONMENT.lower(): "",
    GOOGLE_NEWS_TYPE_ENTERTAINMENT.lower(): "",
    GOOGLE_NEWS_TYPE_FOOD.lower(): "",
    GOOGLE_NEWS_TYPE_ART.lower(): "",
}
GOOGLE_NEWS_URL_MAIN = "https://news.google.com/"


class GoogleNewsScraper:
    """scrape news texts from Google News"""

    def __init__(self, news_type: str = ""):
        news_type = news_type.lower()
        if not news_type in GOOGLE_NEWS_TYPES.keys():
            news_type = GOOGLE_NEWS_TYPE_COMMON
        self.news_type = news_type
        self.news_list = []

    def get_news_list(self) -> list:
        return self.news_list

    def __str__(self) -> str:
        return f"news type: '{self.news_type}', news list: {self.news_list}"

    def scrape(self):
        self.news_list = []
        try:
            # main page
            url = GOOGLE_NEWS_URL_MAIN
            respond = requests.get(url)
            log.info(__name__ + f"{respond}")
            # soup = BeautifulSoup(respond.text, "html.parser")
            # soup.prettify()
            # return {
            #     "error": "ok",
            #     "title": soup.title.get_text(),
            #     "text": soup.get_text(),
            # }
        except Exception as exception:
            log.error(__name__ + f": url: {url}. {exception}")
            # error = f"Can not get page {url}. {exception}"
            # print(error)
            # return {
            #     "error": error,
            # }

        return self
