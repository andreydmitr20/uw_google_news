from django.urls import path, include
from .views import (
    CheckView,
    TestNewsView,
    ScrapeView,
    ClientsView,
    AddClientView,
    ListSMSClientView,
)


urlpatterns = [
    path("api/check/", CheckView.as_view(), name="check_ok"),
    path(
        "api/scrape/",
        ScrapeView.as_view(),
        name="scrape one news by search text",
    ),
    path(
        "api/client/<int:clients_id>/",
        ClientsView.as_view(),
        name="clients",
    ),
    path(
        "api/client/add/",
        AddClientView.as_view(),
        name="add client",
    ),
    path(
        "api/client/list/sms/",
        ListSMSClientView.as_view(),
        name="list clients for sms sending",
    ),
    path("", TestNewsView.as_view(), name="test_news"),
]
