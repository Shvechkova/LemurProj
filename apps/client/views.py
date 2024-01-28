# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from apps.service.models import ServiceClient
from .models import Client, Contract
from .forms import ClientNew, NewServiceClient, AddContract, UpdServiceClient

# from rest_framework import generic
from rest_framework import routers, serializers, viewsets
from .serializers import ClientSerializer


# class ClientIpiView(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer





def clients(request):
    if request.method == "POST":
        form = ClientNew(data=request.POST) 
        
        if form.is_valid():
            
            form.save()
            return HttpResponseRedirect(reverse("clients:index"))
    else:
        form = ClientNew()

    client_list = Client.objects.all()
    title = "Клиенты"
    context = {
        "title": title,
        "client_list": client_list,
        "form": form,
    }
    return render(request, "client/index.html", context)


def client(request, client_id):
    if request.method == "POST" and "window" in request.POST:
        if request.POST["window"] == "service":
            form = NewServiceClient(request.POST)
            if form.is_valid():
                client = form.cleaned_data["client"]
                services_name = form.cleaned_data["services_name"]
                service_new = ServiceClient.objects.create(
                    services_name=services_name,
                    client=client,
                )
        return HttpResponseRedirect(request.path)
    else:
        form = NewServiceClient()

    client = Client.objects.get(id=client_id)
    client_service = ServiceClient.objects.filter(client=client_id)

    context = {
        "client": client,
        "client_service": client_service,
        # "services_name": NewServiceClient,
        "form": form,
    }
    return render(request, "client/client.html", context)


def addContract(request, client_id, slug):
    client = Client.objects.get(id=client_id)
    service = ServiceClient.objects.get(client=client_id, services_name=slug)
    # service_form = ServiceClient.objects.get(client=client_id)
    
    if request.method == "POST":
        form = AddContract(request.POST)
        if form.is_valid():
            contract_number = form.cleaned_data["contract_number"]
            contract_sum = form.cleaned_data["contract_sum"]
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]
            
            service = service
            client = client
            contract_new = Contract.objects.create(
                contract_number=contract_number,
                contract_sum=contract_sum,
                date_start=date_start,
                date_end=date_end,
             
                service=service,
                client=client,
            )
            return HttpResponseRedirect(request.path)
        else:
            form = AddContract()

    contract = Contract.objects.filter(client=client_id)
    form = AddContract()
    context = {
        "client": client,
        "service": service,
        "contract": contract,
        "form": form,
    }
    return render(request, "client/add_contract.html", context)


# def AddSubcontractors(request, client_id, slug):
#     client = Client.objects.get(id=client_id)
#     service = ServiceClient.objects.get(client=client_id, services_name=slug)
#     subcontractor = SubcontractAll.objects.filter(service_client_id=service)
#     form = AddSubPeople()

#     if request.method == "POST":
#         form = AddSubPeople(request.POST)
#         if form.is_valid():
#             seosub_people = form.cleaned_data["seosub_people"]
#             seosub_sum = form.cleaned_data["seosub_sum"]

#             service_client = service

#             contract_new = SubcontractAll.objects.create(
#                 seosub_people=seosub_people,
#                 seosub_sum=seosub_sum,
#                 service_client=service_client,
#             )
#             return HttpResponseRedirect(request.path)
#         else:
#             form = AddSubPeople()
#     print(subcontractor)
#     context = {
#         "client": client,
#         "service": service,
#         "subcontractor": subcontractor,
#         # # "services_name": NewServiceClient,
#         "form": form,
#     }

#     return render(request, "client/add_sub.html", context)


# def add_employee(request, client_id, slug):
#     client = Client.objects.get(id=client_id)
#     service = ServiceClient.objects.get(client=client_id, services_name=slug)
#     # subcontractor = SubcontractAll.objects.filter(service_client_id=service)
#     form = EmployeeDevNew()

#     if request.method == "POST" and "window" in request.POST:
#         if request.POST["window"] == "dv":
#             form = EmployeeDevNew(request.POST)
#             if form.is_valid():
#                 drvsub_people = form.cleaned_data["drvsub_people"]
#                 drvsub_sum = form.cleaned_data["drvsub_sum"]

#                 service_client = service

#                 contract_new = SubcontractAll.objects.create(
#                     drvsub_people=drvsub_people,
#                     drvsub_sum=drvsub_sum,
#                     service_client=service_client,
#                 )
#                 return HttpResponseRedirect(request.path)

#             else:
#                 form = EmployeeDevNew()

#         if request.POST["window"] == "designer":
#             form = EmployeeDesignNew(request.POST)
#             if form.is_valid():
#                 designersub_people = form.cleaned_data["designersub_people"]
#                 designersub_sum = form.cleaned_data["designersub_sum"]

#                 service_client = service

#                 contract_new = SubcontractAll.objects.create(
#                     designersub_people=designersub_people,
#                     designersub_sum=designersub_sum,
#                     service_client=service_client,
#                 )
#     dev = SubcontractAll.objects.filter(service_client=service)
#     designer = SubcontractAll.objects.filter(service_client=service)

#     context = {
#         "client": client,
#         "service": service,
#         "designer": designer,
#         "dev": dev,
#         "form": form,
#     }

#     return render(request, "client/add_employee.html", context)


# def add_adv(request, client_id, slug):
#     client = Client.objects.get(id=client_id)
#     service = ServiceClient.objects.get(client=client_id, services_name=slug)

#     form = AddAdvService()

#     if request.method == "POST" and "window" in request.POST:
#         if request.POST["window"] == "adv":
#             form = AddAdvService(request.POST)
#             if form.is_valid():
#                 adv_name = form.cleaned_data["adv_name"]
#                 adv_new = SubcontractADV.objects.create(
#                     adv_name=adv_name,
#                     service_client=service,
#                 )

#             return HttpResponseRedirect(request.path)

#         elif request.POST["window"] == "add_all_sum_adv":
#             form = UpdServiceClient(request.POST)

#             if form.is_valid():
#                 adv_all_sum = form.cleaned_data["adv_all_sum"]
#                 id_service = form.cleaned_data["id_service"]
#                 adv_new_sum = ServiceClient.objects.filter(id=id_service).update(
#                     adv_all_sum=adv_all_sum
#                 )

#             return HttpResponseRedirect(request.path)
#     else:
#         form = AddAdvService()

#     # adv_sum = ServiceClient.objects.filter(id=28)
#     service_client_id = ServiceClient.objects.filter(client_id=client_id).filter(
#         services_name=slug
#     )

#     service_client_id2 = ServiceClient.objects.filter(client_id=client_id).get(
#         services_name=slug
#     )

#     sub_adv = SubcontractADV.objects.filter(service_client=service_client_id2)

#     context = {
#         "client": client,
#         "service": service,
#         "service_client_id": service_client_id,
#         "sub_adv": sub_adv,
#         "service_client_id2": service_client_id2,
#         "form": form,
#     }

#     return render(request, "client/add_adv.html", context)
