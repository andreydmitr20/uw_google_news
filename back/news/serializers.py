from rest_framework import serializers


from .models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    """ClientsSerializer"""

    class Meta:
        model = Clients
        fields = "__all__"


class ListSMSClientSerializer(serializers.ModelSerializer):
    """ListSMSClientSerializer"""

    class Meta:
        model = Clients
        fields = ["email", "phone"]


class EmptySerializer(serializers.Serializer):
    pass
