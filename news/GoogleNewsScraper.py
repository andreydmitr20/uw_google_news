from urllib.parse import urlencode
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from mylib.log import current_utc_date_int, d, int_utc_to_str, log

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
# SELECTOR_ARTICLES = "article a[href*='./articles/']"
SELECTOR_ARTICLES = "article"


class MySelenium:
    def __init__(
        self,
        selenium_driver,
    ) -> None:
        self.__driver = selenium_driver
        self.__actions = None

    def get_driver(self):
        return self.__driver

    def get_actions(self):
        return self.__actions

    def set_actions(self, actions):
        self.__actions = actions

    # click
    def click(self, element):
        if element:
            self.__actions.move_to_element(element).click().perform()

    # findElement
    def find_element_by_css(self, element, css_selector: str):
        if element:
            try:
                return element.find_element(By.CSS_SELECTOR, css_selector)
            except Exception as exception:
                return None

    def find_elements_by_css(self, element, css_selector: str):
        if element:
            try:
                return element.find_elements(By.CSS_SELECTOR, css_selector)
            except Exception as exception:
                return []

    def find_element_by_xpath(self, element, xpath_selector: str):
        if element:
            try:
                return element.find_element(By.XPATH, xpath_selector)
            except Exception as exception:
                return None

    def find_elements_by_xpath(self, element, xpath_selector: str):
        if element:
            try:
                return element.find_elements(By.XPATH, xpath_selector)
            except Exception as exception:
                return []

    # send_keys
    def send_keys(self, element, keys):
        element.send_keys(keys)

    # current_url
    def current_url(self):
        return self.__driver.current_url

    # scroll_into_view
    def scroll_into_view(self, element):
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def go_up_to_element_with_css(self, element, css_selector: str):
        if element is None:
            return None
        while True:
            parent = self.find_element_by_xpath(element, "..")
            if parent is None:
                return None
            result = self.find_elements_by_css(parent, css_selector)
            if len(result) > 0:
                return result[0]
            element = parent


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

            log.info(__name__ + f"{first_article.text}")
            # log.info(__name__ + f"{articles_list}")
            time.sleep(10)
        except Exception as exception:
            log.error(__name__ + f" {exception}")
            self.__news_text = ""

        self.__news_utc_date = current_utc_date_int()
        return self
