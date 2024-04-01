from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, mixins, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.operation.api.serializers import OperationEntrySerializer

from apps.operation.models import OperationEntry

# Create your views here.
def operation_outside(request):
    title = "внешние счета"
    category_operation = ...
    context = {
        "title": title,
    }
    return render(request, "operation/operation_outside.html", context)


def operation_inside(request):
    title = "внутренние счета"
    context = {
        "title": title,
    }
    return render(request, "operation/operation_inside.html", context)

def operation_storage(request):
    title = "внутренние счета"
    context = {
        "title": title,
    }
    return render(request, "operation/operation_storage.html", context)


def index(request):
   

    title = ""
    context = {
        
        "title": title,
       
    }
    return render(request, context)
