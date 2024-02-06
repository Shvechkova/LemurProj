from rest_framework import serializers
from apps.service.models import Service, ServicesMonthlyBill

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"        


class ServicesMonthlyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesMonthlyBill
        fields = "__all__"      