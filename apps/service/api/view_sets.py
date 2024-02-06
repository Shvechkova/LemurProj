from django.forms import ValidationError
from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.service.models import Service, ServicesMonthlyBill
from apps.service.api.serializers import (
    ServiceSerializer,
    ServicesMonthlyBillSerializer,
)


class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServicesMonthlyBillView(viewsets.ModelViewSet):
    queryset = ServicesMonthlyBill.objects.all()
    serializer_class = ServicesMonthlyBillSerializer
