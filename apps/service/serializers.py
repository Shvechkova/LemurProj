from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.client.models import Client, Contract
from apps.service.models import ServiceClient


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["client_name"]


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['contract_number', 'contract_sum', 'client', 'date_start','date_end','service','created_timestamp',]


class ContractClient(serializers.ModelSerializer):
    contract = ContractSerializer(read_only=True, many=True)
    ClientSerializer = ContractSerializer(read_only=True, many=True)
    
    
    # class MainSerializer(serializers.ModelSerializer):
    # child = ChildSerializer(read_only=True, many=True)