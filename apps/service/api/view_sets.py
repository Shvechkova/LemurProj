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

# сервисы
class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# месячные счета
class ServicesMonthlyBillView(viewsets.ModelViewSet):
    queryset = ServicesMonthlyBill.objects.all()
    serializer_class = ServicesMonthlyBillSerializer
    http_method_names = ["get", "post", "put", 'delete']

    # список счетов
    @action(detail=False, methods=["post"],  url_path=r"new_month")
    def subcontract_list(self, request):
        print(1231)
        data = request.data

        bill_now_mohth = ServicesMonthlyBill.objects.filter(
            service=data['service'], created_timestamp__year=data['year'], created_timestamp__month=data['month'])

        return Response()

    # @action(detail=False, methods=["post", "put"], url_path=r"upd_subs")
    # def upd_contracts(
    #     self,
    #     request,
    #     *args,
    #     **kwargs,
    # ):
    #     data = request.data

    #     for contracts in data:
    #         id = contracts["id"]
    #         if id == "":
    #             serializer = self.serializer_class(data=contracts)
    #             if serializer.is_valid():
    #                 serializer.save()
    #         else:
    #             contract = SubcontractMonth.objects.get(pk=id)
    #             serializer = self.serializer_class(
    #                 instance=contract, data=contracts, partial=True
    #             )
    #             if serializer.is_valid():
    #                 serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# категории для адв
class SubcontractCategoryAdvView(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer

# категории других субконтрактов
class SubcontractCategoryOtherView(viewsets.ModelViewSet):
    queryset = SubcontractOther.objects.all()
    serializer_class = SubcontractOtherSerializer

# субконтракты для месячных счетов
class SubcontractMonthView(viewsets.ModelViewSet):
    queryset = SubcontractMonth.objects.all()
    serializer_class = SubcontractMonthSerializer
    http_method_names = ["get", "post", "put", 'delete']

    # прееопределенный делит что бы чекинить суммы в модели
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        idBill = instance.month_bill.id

        billSuborders = SubcontractMonth.objects.filter(
            month_bill=idBill)
        bill = ServicesMonthlyBill.objects.get(id=idBill)

        if billSuborders.count() == 0:
            bill.chekin_add_subcontr = False
            bill.save()
        else:
            bill.chekin_add_subcontr = True
            bill.save()

            # operation = Operation.objects.filter(
            #     monthly_bill=idBill, type_operation='entry').aggregate(total=Sum('amount', default=0))

            # if operation['total'] == billNeedSumEntry.contract_sum:
            #     billNeedSumEntry.chekin_sum_entrees = True
            #     billNeedSumEntry.save()
            # else:
            #     billNeedSumEntry.chekin_sum_entrees = False
            #     billNeedSumEntry.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # создание субконтракта

    @action(detail=False, methods=["post", "put"], url_path=r"add")
    def create_subcontracts(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # список субкнтрактов

    @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/subcontract_li")
    def subcontract_list(self, request, pk):
        pk = self.kwargs["pk"]
        queryset = SubcontractMonth.objects.filter(month_bill=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    # апгрейт субконтракта

    @action(detail=False, methods=["post", "put"], url_path=r"upd_subs")
    def upd_contracts(
        self,
        request,
        *args,
        **kwargs,
    ):
        data = request.data

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
