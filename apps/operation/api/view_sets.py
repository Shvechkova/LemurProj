from apps.operation.api.serializers import OperationEntrySerializer, OperationOutSerializer, OperationSerializer
from apps.operation.models import Operation, OperationEntry, OperationOut

from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


class OperationEntryViews(viewsets.ModelViewSet):
    queryset = OperationEntry.objects.all()
    serializer_class = OperationEntrySerializer
    http_method_names = ["get", "post",]
    
    @action(detail=False, methods=["post"], url_path=r"contract_filter_list")
    def operation_entry_filter(
        self,
        request,
    ):
     
        data =  request.data
        obj = []
        for data_item in data:
        
            queryset = OperationEntry.objects.filter(id=data_item['id'])
            serializer = self.serializer_class(queryset, many=True)
            obj.append(serializer.data)
        
        print(obj)   
        return Response(obj)
    
class OperationOutViews(viewsets.ModelViewSet):
    queryset = OperationOut.objects.all()
    serializer_class = OperationOutSerializer
    http_method_names = ["get", "post",] 
    
    @action(detail=False, methods=["post"], url_path=r"operation_out_filter")
    def operation_out_filter(
        self,
        request,
    ):
     
        data =  request.data
        queryset = OperationOut.objects.filter(suborder=data['id'])
        serializer = self.serializer_class(queryset, many=True)
           
        return Response(serializer.data) 
    
    
    
class OperationViews(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    http_method_names = ["get", "post",]
    
    @action(detail=False, methods=["post"], url_path=r"operation_entry_list")
    def operation_entry_filter(
        self,
        request,
    ):
     
        data =  request.data
        obj = []
        for data_item in data:
        
            queryset = Operation.objects.filter(id=data_item['id'])
            serializer = self.serializer_class(queryset, many=True)
            obj.append(serializer.data)
        
        print(obj)   
        return Response(obj)      
   