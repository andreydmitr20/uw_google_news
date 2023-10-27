from django.urls import path, include
from .views import CheckView, TestNewsView, ScrapeView

urlpatterns = [
    path("api/check/", CheckView.as_view(), name="check_ok"),
    path(
        "api/scrape/",
        ScrapeView.as_view(),
        name="scrape one news by search text",
    ),
    path("", TestNewsView.as_view(), name="test_news"),
]
