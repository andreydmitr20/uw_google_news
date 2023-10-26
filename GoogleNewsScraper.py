from log import log

GOOGLE_NEWS_TYPE_COMMON = "common"
# GOOGLE_NEWS_TYPE_COMMON = "common"
GOOGLE_NEWS_TYPES = {GOOGLE_NEWS_TYPE_COMMON: ""}


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
        self.news_list = ["test"]
        return self
