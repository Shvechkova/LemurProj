from rest_framework import serializers
from apps.service.models import Adv, Service, ServicesMonthlyBill, SubcontractMonth, SubcontractOther


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServicesMonthlyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesMonthlyBill
        fields = "__all__"


class SubcontractMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcontractMonth
        fields = "__all__"


class AdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adv
        fields = "__all__"


class SubcontractOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcontractOther
        fields = "__all__"
