from rest_framework import serializers


from .models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    """ClientsSerializer"""

    class Meta:
        model = Clients
        fields = "__all__"


class EmptySerializer(serializers.Serializer):
    pass
