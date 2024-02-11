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
    month_bill_all = ServicesMonthlyBill.objects.all()
    month_bill_last = ServicesMonthlyBill.objects.latest('created_timestamp')
    
    category_service = Service.objects.get(name=slug)
    client = Client.objects.filter(contract__service=category_service.id)

    ordered_bill = ServicesMonthlyBill.objects.filter(service=category_service)

    total_income = ServicesMonthlyBill.objects.filter(service=category_service).annotate(month=TruncMonth(
        'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__contract_sum'))

    total_adv = ServicesMonthlyBill.objects.filter(service=category_service).annotate(month=TruncMonth(
        'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__adv_all_sum'))

    suncontr_adv = ServicesMonthlyBill.objects.filter(service=category_service).annotate(month=TruncMonth(
        'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__adv_all_sum'))

    subcontractors = SubcontractMonth.objects.all()
    advCategory = Adv.objects.all()

   
    title = category_service.id
    context = {
        "title": title,
        "client": client,
        "month_bill_all": month_bill_all,
        "category_service": category_service,
        "ordered_bill": ordered_bill,
        'total_income': total_income,
        'total_adv': total_adv,
        'subcontractors': subcontractors,
        'adv_category': advCategory,
        'month_bill_last': month_bill_last,



    }
    return render(request, "service/one_service.html", context)


# def serviced(request, slug):
#     service_client = ServiceClient.objects.filter(services_name=slug)
#     actual_contract = Contract.objects.filter(service__in=service_client)

#     if request.method == "POST" and "window" in request.POST:
#         if request.POST["window"] == "add_cash_contract":
#             form = OperationEntryForm(request.POST)
#             if form.is_valid():
#                 id_contract = form.cleaned_data["id_contract"]
#                 comment = form.cleaned_data["comment"]
#                 amount = form.cleaned_data["amount"]
#                 bank = form.cleaned_data["bank"]
#                 operation_entry_new = OperationEntry.objects.create(
#                     sum=amount, contract_id=id_contract, comment=comment
#                 )
#                 operation_entry_last = OperationEntry.objects.latest("id")
#                 print(operation_entry_last)
#                 bank_operation_new = BankAll.objects.create(
#                     operation_entry_id=operation_entry_last.id,
#                     name=bank,
#                 )
#                 return HttpResponseRedirect(request.path)

#     operation_entry_chek = OperationEntry.objects.all()
#     sub_adv_actual = SubcontractADV.objects.all()
#     sub_all_actual = SubcontractAll.objects.all()
#     title = "Одна услуга"
#     context = {
#         "title": slug,
#         "service_client": service_client,
#         "actual_contract": actual_contract,
#         "operation_entry_chek": operation_entry_chek,
#         # 'form': form,
#         "sub_adv_actual": sub_adv_actual,
#         "sub_all_actual": sub_all_actual,
#     }

#     return render(request, "service/one_servis.html", context)


# def serviced(request, slug):

#     title = "Одна услуга"
#     context = {
#         "title": slug,
#         'request':request,
#     }

#     return render(request, "service/one_servis.html", context)
