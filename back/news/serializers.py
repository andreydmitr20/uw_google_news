from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MinValueValidator,
    MaxValueValidator,
)
from rest_framework import serializers

from .models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    """ClientsSerializer"""

    phone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$", message="Enter a valid phone number."
            )
        ]
    )
    email = serializers.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    days_in_week_choices = [1, 2, 3, 7]
    days_in_week = serializers.ChoiceField(choices=days_in_week_choices)

    news_type = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[a-z]+$", message="Only lowercase English letters are allowed."
            )
        ]
    )

    class Meta:
        model = Clients
        fields = "__all__"


class ListSMSClientSerializer(serializers.ModelSerializer):
    """ListSMSClientSerializer"""

    class Meta:
        model = Clients
        fields = ["clients_id", "phone"]


class EmptySerializer(serializers.Serializer):
    pass
