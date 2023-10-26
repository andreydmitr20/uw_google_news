from .mylib.log import log, d, current_utc_date_int, int_utc_to_str
from urllib.parse import urlencode


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
GOOGLE_NEWS_URL_SEARCH = "https://news.google.com/search?"

SELECTOR_MENUBAR_LINKS = 'div[role="menubar"] a'
SELECTOR_ARTICLES = "article a[href*='article']"


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

    def scrape_by_search(self, search_text: str):
        try:
            # get search page
            url = GOOGLE_NEWS_URL_SEARCH + urlencode({"q": search_text})
            # log.info(__name__ + f" {url}")
            soup = self.get_page(url)

            # scripts = soup.select("script")
            # # log.info(__name__ + f" {scripts}")

            # url = None
            # for script in scripts:
            #     text = script.text
            #     # index_function = text.find("AF_initDataCallback")
            #     # if index_function < 0:
            #     #     continue
            #     # print("\n")
            #     stop_keywords_list = [
            #         "gstatic.com",
            #         "googleusercontent.com",
            #         "google.com",
            #     ]
            #     count = 0
            #     index_current = 0
            #     while True:
            #         index_https = text.find(
            #             '"https://', index_current
            #         )  # , index_function)
            #         if index_https < 0:
            #             break
            #         index_quotas = text.find('"', index_https + 1)
            #         if index_quotas < 0:
            #             break
            #         url = text[index_https + 1 : index_quotas]
            #         index_current = index_quotas + 1
            #         count += 1
            #         if count == 1:
            #             print()
            #         # print(f"{count}. {url}\n")

            #         is_stop_keyword_found = False
            #         for keyword in stop_keywords_list:
            #             if url.find(keyword) >= 0:
            #                 is_stop_keyword_found = True
            #                 break
            #         if is_stop_keyword_found:
            #             if count == 10:
            #                 break
            #             continue

            #         print(f"{count} {url}\n")

            # log.info(__name__ + f" {text[index_https:index_https+20]}")

            articles_links = soup.select(SELECTOR_ARTICLES)
            if len(articles_links) == 0:
                raise Exception(f" No articles by search '{search_text}'")

            # get news page
            link = articles_links[0]
            url = GOOGLE_NEWS_URL_MAIN + link.get("href")[2:]
            log.info(__name__ + f" {url}")
            soup = self.get_page(url)
            log.info(__name__ + f" {soup.text}")

        except Exception as exception:
            log.error(__name__ + f": url: {url}. {exception}")

        self.__news_utc_date = current_utc_date_int()
        return self
