from urllib.parse import urlencode
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .mylib.log import current_utc_date_int, d, int_utc_to_str, log

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
GOOGLE_NEWS_URL_SEARCH = "https://news.google.com/search?"

SELECTOR_MENUBAR_LINKS = 'div[role="menubar"] a'
SELECTOR_ARTICLES = "article a[href*='article']"


class GoogleNewsScraper:
    """scrape news texts from Google News"""

    def __init__(
        self,
        selenium_driver,
        search_text: str = "",
    ):
        self.__news_utc_date = current_utc_date_int()
        self.__driver = selenium_driver
        self.__url = GOOGLE_NEWS_URL_SEARCH + urlencode({"q": search_text})
        self.__actions = None
        self.__news_text = ""

    def get_driver(self) -> str:
        return self.__driver

    def get_actions(self) -> list:
        return self.__actions

    def get_news_utc_date(self) -> int:
        return self.__news_utc_date

    def get_news_text(self) -> str:
        return self.__news_text

    def scrape_by_search(self, search_text: str):
        self.__news_text = ""
        try:
            self.__driver.get(self.__url)
            self.__actions = ActionChains(self.__driver)

            time.sleep(10)
        except Exception as exception:
            log.error(__name__ + f" {exception}")
            self.__actions = None
            self.__news_text = ""

        self.__news_utc_date = current_utc_date_int()
        return self
        # try:
        #     # get search page
        #     url = GOOGLE_NEWS_URL_SEARCH + urlencode({"q": search_text})
        #     # log.info(__name__ + f" {url}")
        #     soup = self.get_page(url)

        #     # scripts = soup.select("script")
        #     # # log.info(__name__ + f" {scripts}")

        #     # url = None
        #     # for script in scripts:
        #     #     text = script.text
        #     #     # index_function = text.find("AF_initDataCallback")
        #     #     # if index_function < 0:
        #     #     #     continue
        #     #     # print("\n")
        #     #     stop_keywords_list = [
        #     #         "gstatic.com",
        #     #         "googleusercontent.com",
        #     #         "google.com",
        #     #     ]
        #     #     count = 0
        #     #     index_current = 0
        #     #     while True:
        #     #         index_https = text.find(
        #     #             '"https://', index_current
        #     #         )  # , index_function)
        #     #         if index_https < 0:
        #     #             break
        #     #         index_quotas = text.find('"', index_https + 1)
        #     #         if index_quotas < 0:
        #     #             break
        #     #         url = text[index_https + 1 : index_quotas]
        #     #         index_current = index_quotas + 1
        #     #         count += 1
        #     #         if count == 1:
        #     #             print()
        #     #         # print(f"{count}. {url}\n")

        #     #         is_stop_keyword_found = False
        #     #         for keyword in stop_keywords_list:
        #     #             if url.find(keyword) >= 0:
        #     #                 is_stop_keyword_found = True
        #     #                 break
        #     #         if is_stop_keyword_found:
        #     #             if count == 10:
        #     #                 break
        #     #             continue

        #     #         print(f"{count} {url}\n")

        #     # log.info(__name__ + f" {text[index_https:index_https+20]}")

        #     articles_links = soup.select(SELECTOR_ARTICLES)
        #     if len(articles_links) == 0:
        #         raise Exception(f" No articles by search '{search_text}'")

        #     # get news page
        #     link = articles_links[0]
        #     url = GOOGLE_NEWS_URL_MAIN + link.get("href")[2:]
        #     log.info(__name__ + f" {url}")
        #     soup = self.get_page(url)
        #     log.info(__name__ + f" {soup.text}")

        # except Exception as exception:
        #     log.error(__name__ + f": url: {url}. {exception}")
