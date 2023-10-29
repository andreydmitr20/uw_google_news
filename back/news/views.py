from django.db.models import F, Q
from django.shortcuts import render
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from .serializers import EmptySerializer
from tasks.news.news import news_scraper


PERMISSION_CLASSES = [AllowAny]
# PERMISSION_CLASSES=[IsAuthenticated]


@extend_schema(tags=["check ok"])
class CheckView(GenericAPIView):
    """check ok"""

    permission_classes = [AllowAny]
    queryset = []
    serializer_class = EmptySerializer

    @extend_schema(
        description="check ok",
        # parameters=[
        #     OpenApiParameter("url", description='url'),
        # ],
    )
    def get(self, request, format=None):
        # result = get_page(request.GET.get("url"))
        return Response([{"api_status": "ok"}], status=status.HTTP_200_OK)


@extend_schema(tags=["get one news by search text"])
class ScrapeView(GenericAPIView):
    """ScrapeView"""

    permission_classes = [AllowAny]
    queryset = []
    serializer_class = EmptySerializer

    @extend_schema(
        description="scrape one news",
        parameters=[
            OpenApiParameter("search", description="search text for news"),
        ],
    )
    def get(self, request, format=None):
        search_text = request.GET.get("search")
        if search_text:
            print(">1>")
            result = news_scraper.delay(search_text)
            print(">2>")

            try:
                print(">3>")

                output_data = result.get(timeout=80)
                if output_data and isinstance(output_data, dict):
                    return Response([output_data], status=status.HTTP_200_OK)
                raise Exception("Bad result")
            except Exception as exception:
                return Response(
                    [{"error": f"{exception}"}], status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            [{"error": "no param 'search'"}], status=status.HTTP_400_BAD_REQUEST
        )


class TestNewsView(View):
    """test page"""

    def get(self, request, *args, **kwargs):
        # Your processing logic here

        # Rendering the HTML file
        return render(request, "index.html", context={"variable": "value"})
