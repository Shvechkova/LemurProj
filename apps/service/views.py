from ctypes import cast
import datetime
from itertools import groupby
from math import sumprod
from django.forms import DateField
from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
# from apps import service

from operator import itemgetter
from itertools import groupby


from apps.client.models import AdditionalContract, Client

from apps.operation.models import OperationEntry
from apps.service.forms import OperationEntryForm

from apps.service.models import Adv, Service, ServicesMonthlyBill, SubcontractMonth
from rest_framework import routers, viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

# from apps.service.serializers import ClientAllSerializer, ContractSerializer
from rest_framework import status

from apps.service.serializers import ServiceSerializer


def index(request):
    # month_bill_all = ServicesMonthlyBill.objects.all()
    title = "Услуги"
    context = {
        "title": title,
        # "month_bill_all": month_bill_all,
    }
    return render(request, "service/service.html", context)


def service_one(request, slug):
   
    category_service = Service.objects.get(name=slug)
  
    # ordered_bill = ServicesMonthlyBill.objects.filter(service=category_service).order_by("-created_timestamp")
    ordered_bill = ServicesMonthlyBill.objects.filter(service=category_service).prefetch_related('additional_contract',"client").order_by("-created_timestamp")

    total_income = ServicesMonthlyBill.get_total_income(category_service)
    total_adv = ServicesMonthlyBill.get_total_income_adv(category_service)
    
    total_sub = ServicesMonthlyBill.get_total_income_suborder(category_service)
    

   
    subcontractors = SubcontractMonth.objects.all()
    operation_entry = OperationEntry.objects.all()
    advCategory = Adv.objects.all()

    # bill = (
    #     ordered_bill.annotate(month=TruncMonth(
    #     'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__adv_all_sum'))
    #     )
    
    # print(bill)
    # total_sub_adv = (
    #         ordered_bill.all().annotate(total_amount=Sum('subcontractmonth__amount'))
    #     )
    
    dfff = ServicesMonthlyBill.objects.dates('created_timestamp', 'month')
   
    bill = ServicesMonthlyBill.objects.filter().dates('created_timestamp', 'month')
   
   
    title = category_service.id
    context = {
        "title": title,
        
        "category_service": category_service,
        "ordered_bill": ordered_bill,
        'total_income': total_income,
        'total_adv': total_adv,
        'subcontractors': subcontractors,
        'adv_category': advCategory,
        'operation_entry': operation_entry,
      
    }
    return render(request, "service/one_service.html", context)


