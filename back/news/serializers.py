from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MinValueValidator,
    MaxValueValidator,
)
from rest_framework import serializers
from re import match

from .models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    """ClientsSerializer"""

    def validate_phone(self, value):
        regex = r"^\+?1?\d{9,15}$"
        if not match(regex, value):
            raise serializers.ValidationError("Enter a valid phone number.")

        return value

    email = serializers.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    def validate_days_in_week(self, value):
        DAYS_IN_WEEK_CHOICES = [1, 2, 3, 7]
        if value is None or not value in DAYS_IN_WEEK_CHOICES:
            raise serializers.ValidationError(
                "Please enter a valid message delivery frequency per week (1, 2, 3, or 7)."
            )

        return value

    def validate_news_type(self, value):
        regex = r"^[a-z]+$"
        if value is None or value == "":
            raise serializers.ValidationError("Please select at least one interest.")
        if not match(regex, value):
            raise serializers.ValidationError(
                "In interests only lowercase English letters are allowed."
            )

        return value

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
