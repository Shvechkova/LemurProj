from typing import Self
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.client.models import AdditionalContract
from apps.service.models import Service, ServicesMonthlyBill


# class ClientSerializer(serializers.ModelSerializer):
#     # pk = serializers.ReadOnlyField(source='id')
#     class Meta:
#         model = Client
#         fields = "__all__"
#         # fields = ["id","client_name",]


# class ClientAllSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = "__all__"


# class ServicesMonthlyBillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServicesMonthlyBill
#         fields = "__all__"
        
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"        


# class ContractSerializer(serializers.ModelSerializer):
#     # month_bill = ServicesMonthlyBillSerializer(read_only=True, many=True)
#     def create(self, data):
#         # client = data.get('client')
#         # service = data.get('service')
#         # contract_number =data.get('contract_number')
#         # contract_sum = data.get('contract_sum')
#         # adv_all_sum =data.get('adv_all_sum')

#         contract = AdditionalContract.objects.create(**data)
#         # month_bill_save = ServicesMonthlyBill.objects.create(**data)
#         return contract

#     class Meta:
#         model = AdditionalContract
#         fields = [
#             "contract_number",
#             "contract_sum",
#             "client",
#             "service",
#             "created_timestamp",
#             "adv_all_sum",
#         ]


# class ContractClient(serializers.ModelSerializer):
#     contract = ContractSerializer(read_only=True, many=True)
#     ClientSerializer = ContractSerializer(read_only=True, many=True)

    # class MainSerializer(serializers.ModelSerializer):
    # child = ChildSerializer(read_only=True, many=True)
