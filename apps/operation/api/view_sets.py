from apps.operation.api.serializers import OperationEntrySerializer, OperationOutSerializer
from apps.operation.models import OperationEntry, OperationOut

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
   