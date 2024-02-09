from apps.operation.api.serializers import OperationEntrySerializer
from apps.operation.models import OperationEntry

from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


class OperationEntryView(viewsets.ModelViewSet):
    queryset = OperationEntry.objects.all()
    serializer_class = OperationEntrySerializer
    http_method_names = ["get", "post", ]
    
    # created_timestamp
    # comment
    # amount
    # nameNameOperation
    
    # category
    
    # comment