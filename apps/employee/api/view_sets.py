from unicodedata import category
from apps.employee.api.serializers import EmployeeSerializer
from apps.employee.models import Employee
from apps.operation.api.serializers import CategoryOperationSerializer,  OperationSerializer
from apps.operation.models import CategoryOperation, Operation

from rest_framework import routers, serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

import datetime
from dateutil.relativedelta import relativedelta



class EmployeeViews(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    http_method_names = ["get", "post", "delete","put"]