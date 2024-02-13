from django.forms import ValidationError
from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.service.models import Adv, Service, ServicesMonthlyBill, SubcontractMonth, SubcontractOther
from apps.service.api.serializers import (
    AdvSerializer,
    ServiceSerializer,
    ServicesMonthlyBillSerializer,
    SubcontractMonthSerializer,
    SubcontractOtherSerializer,
)


class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServicesMonthlyBillView(viewsets.ModelViewSet):
    queryset = ServicesMonthlyBill.objects.all()
    serializer_class = ServicesMonthlyBillSerializer
    
class SubcontractCategoryAdvView(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer
    
    
class SubcontractCategoryOtherView(viewsets.ModelViewSet):
    queryset = SubcontractOther.objects.all()
    serializer_class = SubcontractOtherSerializer     
    
    
class SubcontractMonthView(viewsets.ModelViewSet):
    queryset = SubcontractMonth.objects.all()
    serializer_class = SubcontractMonthSerializer
    http_method_names = ["get", "post", "put"]  
    
    @action(detail=False, methods=["post", "put"], url_path=r"add")
    def create_subcontracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
