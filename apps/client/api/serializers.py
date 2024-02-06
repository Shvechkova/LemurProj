from rest_framework import serializers

from apps.client.models import AdditionalContract, Client, Contract
from apps.employee.models import Employee


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
        
        
class AdditionalContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalContract
        fields = "__all__"
           
   