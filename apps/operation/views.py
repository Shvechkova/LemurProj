from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, mixins, status
from django.forms import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.operation.api.serializers import OperationEntrySerializer

from apps.operation.models import OperationEntry

# Create your views here.
