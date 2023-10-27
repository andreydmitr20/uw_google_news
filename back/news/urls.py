from django.urls import path, include
from .views import CheckView, TestNewsView

urlpatterns = [
    path("check/", CheckView.as_view(), name="check_ok"),
    path("", TestNewsView.as_view(), name="test_news"),
]
