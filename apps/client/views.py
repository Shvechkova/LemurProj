# from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from apps.employee.models import Employee
from apps.service.models import Service, ServiceClient
from apps.service.serializers import ServiceSerializer
from .models import Client, Contract
from django.db.models import F, Q

# from rest_framework
from rest_framework import routers, serializers, viewsets, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
# from .serializers import ClientSerializer, ContractSerializer, ManagerSerializer


def clients(request):
    print(request.COOKIES.get('sortClient'))
    if request.COOKIES.get('sortClient') != "client":
        sortClient = request.COOKIES["sortClient"]
        contracts = Contract.objects.filter(
        Q(service__name=sortClient)).order_by("service")
    else:
        sortClient = 'client'
        contracts = Contract.objects.all().select_related("client","service",'manager').order_by("client")
        # .order_by("client")
        

    # clients = Client.objects.all()
    
    servise = Service.objects.all()
    
    title = "Клиенты"
    context = {
        # "clients": clients,
        "contracts": contracts,
        "title": title,
        "servise":servise,
    }
    return render(request, "client/index.html", context)


# class AddClient(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer

#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.serializer_class(data=request.data)
#     #     if serializer.is_valid():
#     #         obj = serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=False, methods=["get"], url_path=r"manager_list")
#     # TODO НИЖНЕЕ ПОДЧЕРКИВАНИЕ и с маленьких букв
#     def ManagerList(
#         self,
#         request,
#     ):
#         manager = Employee.objects.filter(category_id=1)
#         serializer = ManagerSerializer(manager, many=True)
#         return Response(serializer.data)


# class ContractView(viewsets.ModelViewSet):
#     queryset = Contract.objects.all()
#     serializer_class = ContractSerializer
#     http_method_names = ["get", "post", "put"]

#     # def list(self, request):
#     #     data=request.data
#     #     print(data)
#     #     queryset = Contract.objects.filter(client_id=data)
#     #     serializer = ContractSerializer(queryset, many=True)
#     #     return Response(serializer.data)

#     @action(detail=False, methods=["get"], url_path=r"(?P<pk>\d+)/contract_li")
#     def client_contract_list(self, request, pk):
#         pk = self.kwargs["pk"]
#         queryset = Contract.objects.filter(client=pk)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=["post", "put"], url_path=r"create_contracts")
#     def create_contracts(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, many=True)
#         if serializer.is_valid():
#             obj = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=["get"], url_path=r"service_list")
    # def ServiceList(
    #     self,
    #     request,
    # ):
    #     service = Service.objects.all()
    #     serializer = ServiceSerializer(service, many=True)

    #     return Response(serializer.data)

    # @action(detail=False, methods=["post"], url_path=r"add_contract")
    # def addContract(self, request, *args, **kwargs):

    #     serializer_class = ClientAddSerializer
    #     serializer = serializer_class(data=data, many=True)
    #     # for datai_tems in serializer.data:
    #     #     data_detali =datai_tems
    #     #     return data_detali

    #     # print(serializer)
    #     # data_client = {
    #     #     "contract_number": serializer.client

    #     # }

    #     if serializer.is_valid():
    #         obj = serializer.save()
    #         print(1)
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:

    #         print(2)

    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST,)


# class AddClientContract(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientAddSerializer

#     def addContract(self, request, *args, **kwargs):
#         print(request)


# def client(request, client_id):
#     if request.method == "POST" and "window" in request.POST:
#         if request.POST["window"] == "service":
#             form = NewServiceClient(request.POST)
#             if form.is_valid():
#                 client = form.cleaned_data["client"]
#                 services_name = form.cleaned_data["services_name"]
#                 service_new = ServiceClient.objects.create(
#                     services_name=services_name,
#                     client=client,
#                 )
#         return HttpResponseRedirect(request.path)
#     else:
#         form = NewServiceClient()

#     client = Client.objects.get(id=client_id)
#     client_service = ServiceClient.objects.filter(client=client_id)

#     context = {
#         "client": client,
#         "client_service": client_service,
#         # "services_name": NewServiceClient,
#         "form": form,
#     }
#     return render(request, "client/client.html", context)


# def addContract(request, client_id, slug):
#     client = Client.objects.get(id=client_id)
#     service = ServiceClient.objects.get(client=client_id, services_name=slug)
#     # service_form = ServiceClient.objects.get(client=client_id)

#     if request.method == "POST":
#         form = AddContract(request.POST)
#         if form.is_valid():
#             contract_number = form.cleaned_data["contract_number"]
#             contract_sum = form.cleaned_data["contract_sum"]
#             date_start = form.cleaned_data["date_start"]
#             date_end = form.cleaned_data["date_end"]

#             service = service
#             client = client
#             contract_new = Contract.objects.create(
#                 contract_number=contract_number,
#                 contract_sum=contract_sum,
#                 date_start=date_start,
#                 date_end=date_end,

#                 service=service,
#                 client=client,
#             )
#             return HttpResponseRedirect(request.path)
#         else:
#             form = AddContract()

#     contract = Contract.objects.filter(client=client_id)
#     form = AddContract()
#     context = {
#         "client": client,
#         "service": service,
#         "contract": contract,
#         "form": form,
#     }
#     return render(request, "client/add_contract.html", context)


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
