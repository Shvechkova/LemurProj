from apps.operation.api.serializers import CategoryOperationSerializer, OperationEntrySerializer, OperationOutSerializer, OperationSerializer
from apps.operation.models import CategoryOperation, Operation, OperationEntry, OperationOut

from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

from apps.service.models import ServicesMonthlyBill, SubcontractMonth

class CategoryOperationViews(viewsets.ModelViewSet):
    queryset = CategoryOperation.objects.all()
    serializer_class = CategoryOperationSerializer
    


# class OperationEntryViews(viewsets.ModelViewSet):
#     queryset = OperationEntry.objects.all()
#     serializer_class = OperationEntrySerializer
#     http_method_names = ["get", "post",]

#     @action(detail=False, methods=["post"], url_path=r"contract_filter_list")
#     def operation_entry_filter(
#         self,
#         request,
#     ):

#         data =  request.data
#         obj = []
#         for data_item in data:

#             queryset = OperationEntry.objects.filter(id=data_item['id'])
#             serializer = self.serializer_class(queryset, many=True)
#             obj.append(serializer.data)

#         print(obj)
#         return Response(obj)

# class OperationOutViews(viewsets.ModelViewSet):
#     queryset = OperationOut.objects.all()
#     serializer_class = OperationOutSerializer
#     http_method_names = ["get", "post",]

#     @action(detail=False, methods=["post"], url_path=r"operation_out_filter")
#     def operation_out_filter(
#         self,
#         request,
#     ):

#         data =  request.data
#         queryset = OperationOut.objects.filter(suborder=data['id'])
#         serializer = self.serializer_class(queryset, many=True)

#         return Response(serializer.data)

# все операции
class OperationViews(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    http_method_names = ["get", "post", "delete"]
    
    # прееопределенный делит что бы чекинить суммы в модели
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        typeOperation = instance.type_operation
        idBill = instance.monthly_bill.id
        
        billNeedSumEntry = ServicesMonthlyBill.objects.get(
                id=idBill)
    #    чекин полный оплаты от клиента 
        if typeOperation == 'entry':
            
            operation = Operation.objects.filter(
                monthly_bill=idBill, type_operation='entry').aggregate(total=Sum('amount', default=0))
            
            if operation['total'] == billNeedSumEntry.contract_sum:
                billNeedSumEntry.chekin_sum_entrees = True
                billNeedSumEntry.save()
            else:
                billNeedSumEntry.chekin_sum_entrees = False
                billNeedSumEntry.save()

        # чекин полной оплаты субподряда    
        elif typeOperation == "out":
            operation = Operation.objects.filter(
                monthly_bill=idBill, type_operation='out').aggregate(total=Sum('amount', default=0))

            planinSum = SubcontractMonth.objects.filter(
                month_bill=idBill).aggregate(total=Sum('amount', default=0))
            
            if operation['total'] == planinSum['total']:
                billNeedSumEntry.chekin_sum_adv = True
                billNeedSumEntry.save()
            else:
                billNeedSumEntry.chekin_sum_adv = False
                billNeedSumEntry.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    # все операции прихода 
    @action(detail=False, methods=["post"], url_path=r"operation_entry_list")
    def operation_entry_filter(
        self,
        request,
    ):

        data = request.data
        obj = []
        for data_item in data:

            queryset = Operation.objects.filter(id=data_item['id'])
            serializer = self.serializer_class(queryset, many=True)
            obj.append(serializer.data)

        return Response(obj)

    # операция прихода сохранение что бы ставить чекин сумм
    @action(detail=False, methods=["post"], url_path=r"operation_save")
    def operation_add(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        idBill = data['monthly_bill']

        # operation = Operation.objects.filter(
        #     monthly_bill=idBill, type_operation='entry').aggregate(total=Sum('amount', default=0))

        if serializer.is_valid():
            obj = serializer.save()
            billNeedSumEntry = ServicesMonthlyBill.objects.get(
                id=idBill)
            operation = Operation.objects.filter(
                monthly_bill=idBill, type_operation='entry').aggregate(total=Sum('amount', default=0))
        
            if operation['total'] == billNeedSumEntry.contract_sum:
                billNeedSumEntry.chekin_sum_entrees = True
                billNeedSumEntry.save()
            else:
                billNeedSumEntry.chekin_sum_entrees = False
                billNeedSumEntry.save()
       

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     # операция расход сохранение что бы ставить чекин сумм

    @action(detail=False, methods=["post"], url_path=r"operation_out")
    def operation_out(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        idBill = data['monthly_bill']
        idSubs = data['suborder']

        # operation = Operation.objects.filter(
        #     monthly_bill=idBill, type_operation='out').aggregate(total=Sum('amount', default=0))

        if serializer.is_valid():
            obj = serializer.save()
            
            billNeedSumEntry = ServicesMonthlyBill.objects.get(
                id=idBill)
          
            
            operation = Operation.objects.filter(
                monthly_bill=idBill, type_operation='out').aggregate(total=Sum('amount', default=0))
            
            planinSum = SubcontractMonth.objects.filter(
                month_bill=idBill).aggregate(total=Sum('amount', default=0))
       
            if operation['total'] == planinSum['total']:
                billNeedSumEntry.chekin_sum_adv = True
                billNeedSumEntry.save()
            else:
                billNeedSumEntry.chekin_sum_adv = False
                billNeedSumEntry.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r"operation_out_filter")
    def operation_out_filter(
        self,
        request,
    ):

        data = request.data
        queryset = Operation.objects.filter(
            type_operation="out", suborder=data['id'])
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
