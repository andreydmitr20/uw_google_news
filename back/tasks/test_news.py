from news.news import GOOGLE_NEWS_TYPE, news_scraper, log


for search_text in GOOGLE_NEWS_TYPE:
    result = news_scraper(search_text)
    log.info(f"{result['error']}>>>{result['search_text']}>>>{result['sms_text']}")
