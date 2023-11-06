""" functions to help with views and serializers """
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from django.core.paginator import EmptyPage, Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, HttpResponse

API_TEXT_SEARCH = "search"
API_TEXT_PAGE = "page"
API_TEXT_PAGE_SIZE = "page_size"
API_TEXT_SHORT = "short"

DEFAULT_PAGE_SIZE_FOR_PAGINATION = 4
MAX_PAGE_SIZE_FOR_PAGINATION = 20


def to_int(value, default_value):
    """return_none_or_int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default_value


def get_int_request_param(request, key, default_value):
    """get_int_request_param"""
    try:
        value = request.data[key]
    except KeyError as exc:
        raise Http404 from exc
    return to_int(value, default_value)


def search_simple(queryset, search_text: str, search_field):
    """search by max 3 patterns space separated"""
    # print('search:', search_text)
    search_text = search_text.replace("%20", " ")

    search_text = search_text.strip()

    if search_text != "":
        search_text = search_text.split("+")

    search_text_len = len(search_text)
    if search_text_len > 0:
        if search_text_len == 1:
            queryset = queryset.filter(
                Q(**{"{}__icontains".format(search_field): search_text[0].strip()})
            )
        elif search_text_len == 2:
            queryset = queryset.filter(
                Q(**{"{}__icontains".format(search_field): search_text[0].strip()})
                & Q(**{"{}__icontains".format(search_field): search_text[1].strip()})
            )
        else:
            queryset = queryset.filter(
                Q(**{"{}__icontains".format(search_field): search_text[0].strip()})
                | Q(**{"{}__icontains".format(search_field): search_text[1].strip()})
                | Q(**{"{}__icontains".format(search_field): search_text[2].strip()})
            )

    return queryset


def get_page(value, default_value):
    """get_page"""
    if not value is None:
        try:
            return int(value)
        except Exception as exc:
            raise Http404 from exc
    return default_value


def pagination_simple(request, serializer, queryset):
    """pagination_simple"""
    page = get_page(request.query_params.get(API_TEXT_PAGE), 1)
    if page == 0:
        # return count
        return Response([{"count": queryset.count()}], status=status.HTTP_200_OK)

    page_size = get_page(
        request.query_params.get(API_TEXT_PAGE_SIZE), DEFAULT_PAGE_SIZE_FOR_PAGINATION
    )

    page_size = min(page_size, MAX_PAGE_SIZE_FOR_PAGINATION)

    try:
        paginator = Paginator(queryset, page_size)

        serializer = serializer(
            paginator.page(page), many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EmptyPage:
        return Response([], status=status.HTTP_200_OK)


def print_query(is_print_query, queryset):
    """print_query"""
    if is_print_query:
        print(queryset.query)


def order_simple(queryset, order_field):
    """order_simple"""
    if not order_field is None:
        order_field = "-pk"
    return queryset.order_by(order_field)


def select_simple(
    model,
    request,
    id,
    serializer_class,
    short_serializer_class=None,
    search_field=None,
    order_field=None,
    is_print_query=False,
):
    """select_simple"""
    serializer_class_local = (
        short_serializer_class
        if not short_serializer_class is None
        and request.query_params.get(API_TEXT_SHORT, "0") == "1"
        else serializer_class
    )

    fields = serializer_class_local.Meta.fields
    queryset = (
        model.objects.all()
        if isinstance(fields, str)
        else model.objects
        # inner join
        # .select_related('user')
        .values(*fields)
    )

    queryset = filter_simple(queryset, "pk", id)

    if not request.query_params.get(API_TEXT_SEARCH) is None:
        if search_field is None:
            Response([], status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = search_simple(
                queryset, request.query_params.get(API_TEXT_SEARCH), search_field
            )

    queryset = order_simple(queryset, order_field)

    print_query(is_print_query, queryset)

    return pagination_simple(request, serializer_class_local, queryset)


def insert_simple(serializer_class, data):
    """create"""
    serializer = serializer_class(data=data)
    # print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_simple(model, request, id, serializer_class):
    """update"""
    try:
        instance = model.objects.get(pk=id)
    except Exception as exc:
        raise Http404 from exc
    # !!! always partial=True to avoid spontaneously changing field values
    serializer = serializer_class(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


ERROR_WHEN_DELETING = "Error when deleting"


def delete_simple(model, conditions):
    """delete"""
    try:
        instance = model.objects.get(conditions)
        print(instance)
    except Exception as exc:
        raise Http404 from exc
    try:
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except IntegrityError:
        return Response(
            ERROR_WHEN_DELETING + " pk=" + str(instance.pk),
            status=status.HTTP_400_BAD_REQUEST,
        )


def representation_simple(my_fields, instance):
    """representation_simple"""
    representation = {}
    for field in my_fields:
        representation[field] = instance[field]
    return representation


def filter_simple(queryset, field_name, value):
    """filter_simple"""
    if not value is None:
        try:
            value = int(value)
            if value != 0:
                queryset = queryset.filter(**{"{}".format(field_name): value})
        except Exception as exc:
            raise Http404 from exc
    return queryset


def filter_params_simple(queryset, field_name, request):
    """filter_params_simple"""
    return filter_simple(queryset, field_name, request.query_params.get(field_name))


def is_serializer_error_duplicate_value(
    serializer_errors: dict, field_name: str
) -> bool:
    return (
        field_name in serializer_errors
        and serializer_errors[field_name][0].find("already exists") != -1
    )
