
from rest_framework import serializers

from apps.client.models import Client
from apps.service.models import ServiceClient


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("client_name",)
        
        
class ClientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceClient
        fields = ("services_name",)
                
        