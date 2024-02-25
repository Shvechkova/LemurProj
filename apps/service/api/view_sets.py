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
    http_method_names = ["get", "post", "put", 'delete']
    
    
class SubcontractCategoryAdvView(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer
    
    
class SubcontractCategoryOtherView(viewsets.ModelViewSet):
    queryset = SubcontractOther.objects.all()
    serializer_class = SubcontractOtherSerializer     
    
    
class SubcontractMonthView(viewsets.ModelViewSet):
    queryset = SubcontractMonth.objects.all()
    serializer_class = SubcontractMonthSerializer
    http_method_names = ["get", "post", "put",'delete']  
    
    @action(detail=False, methods=["post", "put"], url_path=r"add")
    def create_subcontracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/subcontract_li")
    def subcontract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = SubcontractMonth.objects.filter(month_bill=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post", "put"], url_path=r"upd_subs")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data
        print(data)
        for contracts in data:
            id = contracts["id"]
            if id == "":
                serializer = self.serializer_class(data=contracts)
                if serializer.is_valid():
                    serializer.save()
            else:
                contract = SubcontractMonth.objects.get(pk=id)
                serializer = self.serializer_class(
                    instance=contract, data=contracts, partial=True
                )
                if serializer.is_valid():
                    serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)