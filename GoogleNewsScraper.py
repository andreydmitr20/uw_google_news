from log import log, current_utc_date_int, int_utc_to_str
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
    GOOGLE_NEWS_TYPE_COMMON.lower(): "World",
    GOOGLE_NEWS_TYPE_TECH.lower(): "Technology",
    GOOGLE_NEWS_TYPE_BUSINESS.lower(): "Business",
    GOOGLE_NEWS_TYPE_SCIENCE.lower(): "Science",
    GOOGLE_NEWS_TYPE_HEALTH.lower(): "Health",
    GOOGLE_NEWS_TYPE_SPORTS.lower(): "Sports",
    GOOGLE_NEWS_TYPE_POLITICS.lower(): "",
    GOOGLE_NEWS_TYPE_ENVIRONMENT.lower(): "",
    GOOGLE_NEWS_TYPE_ENTERTAINMENT.lower(): "Entertainment",
    GOOGLE_NEWS_TYPE_FOOD.lower(): "",
    GOOGLE_NEWS_TYPE_ART.lower(): "",
}
GOOGLE_NEWS_URL_MAIN = "https://news.google.com/"

SELECTOR_MENUBAR_LINKS = 'div[role="menubar"] a'


class GoogleNewsScraper:
    """scrape news texts from Google News"""

    def __init__(self, news_type: str = ""):
        news_type = news_type.lower()
        if not news_type in GOOGLE_NEWS_TYPES.keys():
            news_type = GOOGLE_NEWS_TYPE_COMMON
        self.__news_type = news_type
        self.__news_list = []
        self.__news_utc_date = current_utc_date_int()

    def get_news_type(self) -> str:
        return self.__news_type

    def get_news_list(self) -> list:
        return self.__news_list

    def get_news_utc_date(self) -> int:
        return self.__news_utc_date

    def get_news_dict(self) -> dict:
        return {
            "utc_date": self.get_news_utc_date(),
            "type": self.get_news_type(),
            "list": self.get_news_list(),
        }

    def __str__(self) -> str:
        try:
            return f"news: date:{int_utc_to_str(self.__news_utc_date)}, type: '{self.__news_type}', {self.__news_list}"
        except Exception as exception:
            log.error(__name__ + f" {exception}")
            return __name__

    def scrape(self):
        self.__news_list = []
        try:
            # main page
            url = GOOGLE_NEWS_URL_MAIN
            respond = requests.get(url)
            # log.info(__name__ + f" {respond}")
            if respond.status_code < 200 or respond.status_code >= 400:
                raise Exception(f" Response code {respond.status_code}")
            soup = BeautifulSoup(respond.text, "html.parser")
            # soup.prettify()
            menubar_links = soup.select(SELECTOR_MENUBAR_LINKS)
            # log.info(__name__ + f" {menubar_links}")
            url = None
            search_text = GOOGLE_NEWS_TYPES[self.__news_type].lower()
            # search link
            for link in menubar_links:
                text = link.text.lower()
                # log.info(__name__ + f" >>{text}>>{search_text}")

                if text.find(search_text) >= 0:
                    url = GOOGLE_NEWS_URL_MAIN + link.get("href")[2:]
                    break
            # log.info(__name__ + f" {url}")
            if url is None:
                raise Exception(__name__ + f' Menu item "{search_text}" is not found')

            # news page
            self.__news_utc_date = current_utc_date_int()

        except Exception as exception:
            log.error(__name__ + f": url: {url}. {exception}")

        return self
