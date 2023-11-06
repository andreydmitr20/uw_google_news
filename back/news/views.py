import os
from datetime import datetime, timedelta, timezone

from django.db import IntegrityError
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
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
    is_serializer_error_duplicate_value,
)

from config import config

from .models import Clients
from .serializers import ClientsSerializer, EmptySerializer, ListSMSClientSerializer

SMS_TEXT_SUBSCRIPTION_IS_OK = "You have successfully subscribed to news updates on selected topics at myheadlines.ai. Thank you!"
SMS_TEXT_SUBSCRIPTION_IS_UPDATED = (
    "You have successfully updated your subscription at myheadlines.ai. Thank you!"
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


@extend_schema(tags=["clients"])
class ClientsView(APIView):
    """ClientsView"""

    permission_classes = [IsAuthenticated]
    # PERMISSION_CLASSES = [AllowAny]

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
    def send_sms_to_client(self, clients_id: int, phone: str, sms_text: str):
        """send_sms_to_client"""
        log_pid = f"back-{os.getpid()}: "
        try:
            if config.send_sms != "False":
                sid = send_sms(
                    sms_text=sms_text,
                    from_phone=config.from_phone,
                    to_phone=phone,
                )
                if len(sid) != MESSAGE_SID_LENGTH:
                    raise Exception("No good sms message sid returned")

            log.info(log_pid + f"Sended sms to clients_id={clients_id}")

        except Exception as exception:
            log.error(log_pid + f"Failed to send sms to clients_id={clients_id}")

    def post(self, request, format=None):
        """post"""

        data = request.data
        utc_date = datetime.now(timezone.utc)
        utc_now_int = int(utc_date.timestamp())

        phone = (
            data["phone"]
            .replace("-", "")
            .replace(")", "")
            .replace("(", "")
            .replace(" ", "")
        )
        if phone.find("+") != 0:
            phone = "+1" + phone
        data["phone"] = phone
        data["utc_created"] = utc_now_int
        data["utc_updated"] = utc_now_int
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                clients_id = serializer.data["clients_id"]
                self.send_sms_to_client(clients_id, phone, SMS_TEXT_SUBSCRIPTION_IS_OK)
                return Response(
                    [{"clients_id": clients_id}],
                    status=status.HTTP_201_CREATED,
                )

            if is_serializer_error_duplicate_value(serializer.errors, "email"):
                clients_email = data["email"]
                client = get_object_or_404(Clients, email=clients_email)
                clients_id = client.clients_id

                # compare phone number
                if phone != client.phone:
                    return Response(
                        {
                            "phone": "The phone number differs from the one entered during registration."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # try to update settings for a client
                try:
                    data["utc_created"] = client.utc_created
                    data["clients_id"] = client.clients_id

                    serializer = self.serializer_class(client, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        self.send_sms_to_client(
                            clients_id, phone, SMS_TEXT_SUBSCRIPTION_IS_UPDATED
                        )

                        return Response(
                            [{"clients_id": clients_id}],
                            status=status.HTTP_200_OK,
                        )
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                except Exception as exception:
                    return Response(
                        {"error": f"Error updating client data. {exception}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif is_serializer_error_duplicate_value(serializer.errors, "phone"):
                return Response(
                    {
                        "phone": "The client with this email has registered a different phone number."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception:
            return Response(
                {"error": f"{exception}"},
                status=status.HTTP_400_BAD_REQUEST,
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
        # parameters=[
        #     # OpenApiParameter("search", description=""),
        #     OpenApiParameter(
        #         "weekday", description="required - day of week: 1- monday, 7 - sunday"
        #     ),
        #     OpenApiParameter(
        #         "interest", description="required - interest: 'w' - world news, etc."
        #     ),
        #     # OpenApiParameter("day_of_week"),
        # ],
    )
    def list_for_days_in_week(self, weekday: int) -> list:
        WEEK_SCHEDULER = {
            1: [3, 7],  # monday
            2: [2, 7],
            3: [1, 3, 7],
            4: [2, 7],
            5: [3, 7],
            6: [7],
            7: [7],
        }
        return WEEK_SCHEDULER.get(weekday, [])

    def get(self, request, weekday=None, interest=None, format=None):
        """get"""

        try:
            weekday = int(weekday)
        except:
            return Response(
                [{"error": f"'weekday' param should be from 1 to 7 (sunday)"}],
                status=status.HTTP_400_BAD_REQUEST,
            )

        if interest is None or interest.strip() == "" or len(interest) > 1:
            return Response(
                [{"error": f"'inerest' param has to be one character like 'w'"}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        interest = interest.lower()[0]

        queryset = self.model.objects.all()
        queryset = queryset.filter(days_in_week__in=self.list_for_days_in_week(weekday))
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
