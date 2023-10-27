from news.news import GOOGLE_NEWS_TYPE, news_scraper, log


for news_type in GOOGLE_NEWS_TYPE:
    result = {"error": "", "search_text": news_type, "sms_text": ""}
    news_scraper(result)
    log.info(f"{result['error']}>>>{result['search_text']}>>>{result['sms_text']}")
