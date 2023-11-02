from datetime import datetime, timedelta, timezone

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
from tasks.news.mylib.twilio_lib import MESSAGE_SID_LENGTH, send_sms
from tasks.news.news import news_scraper
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

from config import config

from .models import Clients
from .serializers import ClientsSerializer, EmptySerializer, ListSMSClientSerializer

SMS_TEXT_SUBSCRIPTION_IS_OK = "You have successfully subscribed to news updates on selected topics at myheadlines.ai. Thank you!"
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


@extend_schema(tags=["clients"])
class ClientsView(APIView):
    """ClientsView"""

    permission_classes = [IsAuthenticated]
    # PERMISSION_CLASSES = [AllowAny]

    serializer_class = ClientsSerializer
    model = Clients

    @extend_schema(
        description="",
        parameters=[
            # OpenApiParameter("search", description=""),
            OpenApiParameter("page", description=""),
            OpenApiParameter("page_size"),
            # OpenApiParameter("day_of_week"),
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

            try:
                serializer = self.serializer_class(
                    queryset, many=True, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as exception:
                return Response(
                    [{"error": f"{exception}"}], status=status.HTTP_400_BAD_REQUEST
                )

    def post(self, request, clients_id=0, format=None):
        """post"""
        return insert_simple(self.serializer_class, request.data)

    def put(self, request, clients_id=0, format=None):
        """put"""
        return update_simple(self.model, request, clients_id, self.serializer_class)

    def delete(self, request, clients_id=0, format=None):
        """delete"""
        return delete_simple(self.model, Q(pk=clients_id))


@extend_schema(tags=["clients"])
class AddClientView(APIView):
    """AddClientView"""

    # permission_classes = [IsAuthenticated]
    PERMISSION_CLASSES = [AllowAny]

    serializer_class = ClientsSerializer
    model = Clients

    @extend_schema(
        description="",
        # parameters=[
        #     # OpenApiParameter("search", description=""),
        #     OpenApiParameter("page", description=""),
        #     OpenApiParameter("page_size"),
        #     # OpenApiParameter("day_of_week"),
        # ],
    )
    def post(self, request, format=None):
        """post"""
        phone = (
            request.data["phone"]
            .replace("-", "")
            .replace(")", "")
            .replace("(", "")
            .replace(" ", "")
        )
        if phone.find("+") != 0:
            phone = "+1" + phone
        request.data["phone"] = phone

        serializer = self.serializer_class(data=request.data)
        # print(serializer)
        try:
            if serializer.is_valid():
                utc_date = datetime.now(timezone.utc)
                serializer.validated_data["utc_created"] = int(utc_date.timestamp())
                serializer.validated_data["utc_updated"] = int(utc_date.timestamp())
                # serializer.validated_data["utc_payed"] = int(
                #     (utc_date + timedelta(days=30)).timestamp()
                # )

                serializer.save()
                clients_id = serializer.data["clients_id"]
                try:
                    sid = send_sms(
                        sms_text=SMS_TEXT_SUBSCRIPTION_IS_OK,
                        from_phone=config.from_phone,
                        to_phone=phone,
                    )
                    if len(sid) != MESSAGE_SID_LENGTH:
                        raise Exception("No good sms message sid returned")
                except Exception as exception:
                    log.error(f"Failed to send sms to clients_id={clients_id}")
                return Response(
                    [{"clients_id": clients_id}],
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            text = f"{exception}"
            if text.find("email") >= 0:
                return Response(
                    {"email": "Duplicate value"}, status=status.HTTP_400_BAD_REQUEST
                )
            if text.find("phone") >= 0:
                return Response(
                    {"phone": "Duplicate value"}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                [{"error": f"{exception}"}], status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["clients"])
class ListSMSClientView(APIView):
    """ListSMSClientView"""

    permission_classes = [IsAuthenticated]
    # PERMISSION_CLASSES = [AllowAny]

    serializer_class = ListSMSClientSerializer
    model = Clients

    @extend_schema(
        description="",
        parameters=[
            # OpenApiParameter("search", description=""),
            OpenApiParameter(
                "weekday", description="required - day of week: 1- monday, 7 - sunday"
            ),
            OpenApiParameter(
                "interest", description="required - interest: 'w' - world news, etc."
            ),
            # OpenApiParameter("day_of_week"),
        ],
    )
    def get_list_for_days_in_week(self, weekday: int) -> list:
        match weekday:
            case 1:
                return [3, 7]
            case 2:
                return [2, 7]
            case 3:
                return [1, 3, 7]
            case 4:
                return [2, 7]
            case 5:
                return [3, 7]
            case 6:
                return [7]
            case _:
                return [7]

    def get(self, request, format=None):
        """get"""
        queryset = self.model.objects.all()
        weekday = request.GET.get("weekday")
        interest = request.GET.get("interest")
        if weekday is None or interest is None:
            return Response(
                [{"error": f"'weekday' and 'interest' params are required"}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            weekday = int(weekday)
        except:
            return Response(
                [{"error": f"'weekday' param should be from 1 to 7 (sunday)"}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        interest = interest.strip().lower()
        if interest == "" or len(interest) > 1:
            return Response(
                [{"error": f"'inerest' param has to be one character like 'w'"}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = queryset.filter(
            days_in_week__in=self.get_list_for_days_in_week(weekday)
        )
        queryset = queryset.filter(news_type__contains=interest)
        print_query(True, queryset)

        try:
            serializer = self.serializer_class(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(
                [{"error": f"{exception}"}], status=status.HTTP_400_BAD_REQUEST
            )
