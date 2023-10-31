from django.db.models import F, Q
from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.news.mylib.log import log
from tasks.news.news import news_scraper

from .models import Clients
from .serializers import ClientsSerializer, EmptySerializer
from utils.views_functions import (
    API_TEXT_SEARCH,
    API_TEXT_SHORT,
    delete_simple,
    filter_params_simple,
    filter_simple,
    get_int_request_param,
    insert_simple,
    order_simple,
    pagination_simple,
    print_query,
    search_simple,
    select_simple,
    to_int,
    update_simple,
)

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

    NEWS_SCRAPER_SECONDS_TIMEOUT = 120
    permission_classes = [IsAuthenticated]
    # PERMISSION_CLASSES = [AllowAny]

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
            try:
                log.info(
                    "django:"
                    + self.__class__.__name__
                    + f" news_scraper('{search_text}') has started. Timeout:{self.NEWS_SCRAPER_SECONDS_TIMEOUT}s"
                )
                result = news_scraper.delay(search_text)
                # print(">2>")

                output_data = result.get(timeout=self.NEWS_SCRAPER_SECONDS_TIMEOUT)
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


NEWS_TYPE = {
    "w": "Today top world news",
    "t": "Today tech and innovations top news",
    "b": "Today business and finance top news",
    "s": "Today science and discovery top news",
    "h": "Today health and wellness top news",
    "p": "Today sport top news",
    "o": "Today politics and government top news",
    "e": "Today environment and sustainability top news",
    "n": "Today entertainment and culture top news",
    "f": "Today food and lifestyle top news",
    "a": "Today art and fashion top news",
}


@extend_schema(tags=["clients"])
class ClientsView(APIView):
    """ClientsView"""

    # permission_classes = [IsAuthenticated]
    PERMISSION_CLASSES = [AllowAny]

    serializer_class = ClientsSerializer
    model = Clients

    @extend_schema(
        description="clients_id=0 retrieve all records before applying filters",
        parameters=[
            # OpenApiParameter("search", description=""),
            OpenApiParameter("page", description=""),
            OpenApiParameter("page_size"),
            OpenApiParameter("day_of_week"),
        ],
    )
    def get(self, request, clients_id=0, format=None):
        """get"""
        if clients_id == 0:
            return Response([], status=status.HTTP_200_OK)
        else:
            queryset = self.model.objects.all()
            queryset = filter_simple(queryset, "pk", clients_id)

            print_query(True, queryset)

            return pagination_simple(request, self.serializer_class, queryset)

    def post(self, request, clients_id=0, format=None):
        """post"""
        return insert_simple(self.serializer_class, request.data)

    def put(self, request, clients_id=0, format=None):
        """put"""
        return update_simple(self.model, request, clients_id, self.serializer_class)

    def delete(self, request, clients_id=0, format=None):
        """delete"""
        return delete_simple(self.model, Q(pk=clients_id))
