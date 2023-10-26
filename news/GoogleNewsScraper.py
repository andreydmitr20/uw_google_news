from urllib.parse import urlencode
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from mylib.log import current_utc_date_int, d, int_utc_to_str, log
from MySelenium import MySelenium


# GOOGLE_NEWS_TYPES = {
#     GOOGLE_NEWS_TYPE_COMMON.lower(): "World",
#     GOOGLE_NEWS_TYPE_TECH.lower(): "Technology",
#     GOOGLE_NEWS_TYPE_BUSINESS.lower(): "Business",
#     GOOGLE_NEWS_TYPE_SCIENCE.lower(): "Science",
#     GOOGLE_NEWS_TYPE_HEALTH.lower(): "Health",
#     GOOGLE_NEWS_TYPE_SPORTS.lower(): "Sports",
#     GOOGLE_NEWS_TYPE_POLITICS.lower(): "",
#     GOOGLE_NEWS_TYPE_ENVIRONMENT.lower(): "",
#     GOOGLE_NEWS_TYPE_ENTERTAINMENT.lower(): "Entertainment",
#     GOOGLE_NEWS_TYPE_FOOD.lower(): "",
#     GOOGLE_NEWS_TYPE_ART.lower(): "",
# }
GOOGLE_NEWS_URL_SEARCH = "https://news.google.com/search?"

# SELECTOR_MENUBAR_LINKS = 'div[role="menubar"] a'
# SELECTOR_ARTICLES = "article a[href*='./articles/']"
SELECTOR_ARTICLES = "article"


class GoogleNewsScraper(MySelenium):
    """scrape news texts from Google News"""

    def __init__(
        self,
        selenium_driver,
    ):
        super().__init__(selenium_driver)
        self.__news_utc_date = current_utc_date_int()
        self.__search_text = ""
        self.__url = ""
        self.__news_text = ""

    def get_news_utc_date(self) -> int:
        return self.__news_utc_date

    def get_news_text(self) -> str:
        return self.__news_text

    def get_search_text(self) -> str:
        return self.__search_text

    def __str__(self) -> str:
        try:
            return f"news: date:{int_utc_to_str(self.__news_utc_date)}, search: '{self.__search_text}', {self.__news_text}"
        except Exception as exception:
            log.error(__name__ + f" {exception}")
            return __name__

    def scrape_by_search(self, search_text: str):
        self.__news_text = ""
        self.__search_text = search_text
        self.__url = GOOGLE_NEWS_URL_SEARCH + urlencode({"q": search_text})
        try:
            self.get_driver().get(self.__url)
            self.set_actions(ActionChains(self.get_driver()))

            articles_list = self.find_elements_by_css(
                self.get_driver(), SELECTOR_ARTICLES
            )
            if len(articles_list) == 0:
                raise Exception("No articles")
            first_article = articles_list[0]
            log.info(__name__ + f" {first_article.text}")

            self.click(first_article)
            time.sleep(4)
            self.switch_to_tab_index(1)

            body = self.find_element_by_css(self.get_driver(), "body")
            text = body.text
            log.info(__name__ + f" {text}")

            self.__news_text = text

            # time.sleep(10)

        except Exception as exception:
            log.error(__name__ + f" {exception}")
            self.__news_text = ""

        self.__news_utc_date = current_utc_date_int()
        return self
