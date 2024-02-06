from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from apps import service


from apps.client.models import AdditionalContract, Client

from apps.operation.models import OperationEntry
from apps.service.forms import OperationEntryForm

from apps.service.models import Service, ServicesMonthlyBill
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

def adv_index(request):
    month_bill_all = ServicesMonthlyBill.objects.all()
    client = Client.objects.all()
    title = "1"
    context = {
        "title": title,
        "month_bill_all": month_bill_all,
        
       
    }
    return render(request, "service/one_service.html", context)

def service_one(request,tag):
    month_bill_all = ServicesMonthlyBill.objects.all()
    client = Client.objects.all()
    title = "1"
    context = {
        "title": title,
        "month_bill_all": month_bill_all,
        
       
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


def serviced(request, slug):
    title = "Одна услуга"
    context = {
        "title": slug,
    }

    return render(request, "service/one_servis.html", context)
