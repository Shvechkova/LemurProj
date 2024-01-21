# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView

from apps.service.models import ServiceClient
from .models import Client, Contract
from .forms import (ClientNew, NewServiceClient, AddService, AddContract)

# Create your views here.


def clients(request):
    client_list = Client.objects.all()
    title='Клиенты'
    context = {
        'title': title,
        'client_list': client_list,
      
    }
    return render(request, 'client/index.html', context)

def client(request,client_id):
    client = Client.objects.get(id=client_id)

    context = {
        'client': client,
      
    }
    return render(request, 'client/client.html', context)
    # return render(request, 'client/index.html', context)


    # if request.method == "POST" and "window" in request.POST:
    #     # добавить клиента
    #     if request.POST["window"] == "client_add":
    #         form = ClientNew(request.POST)
    #         if form.is_valid():
    #             client_name = form.cleaned_data["client_name"]
    #             client_new = Client.objects.create(
    #                 client_name=client_name
    #             )
    #             return HttpResponseRedirect(request.path)
        # добавить услугу к клиенту
        # if request.POST["window"] == "service_add":
        #     form = AddService(request.POST)
        #     if form.is_valid():
        #         client_id = form.cleaned_data["client_id"]
            
        #     data = {
        #         "service_list": "service_list", 
        #     "services_name": NewServiceClient, "client_id": client_id,
        #     }
            
            
        #     return render(request, "client/index.html", context=data)
        # # параметры услуги   
        # if request.POST["window"] == "service": 
        #    form = NewServiceClient(request.POST)
        # #добавить контракт
        # if request.POST["window"] == "contract":
            # form = AddContract(request.POST)
            # if form.is_valid():
            #     # сlient = form.cleaned_data["сlient"]
            #     contract_number = form.cleaned_data["contract_number"]
            #     contract_sum = form.cleaned_data["client_name"]
            #     contract_new = Contract.objects.create(
            #         сlient=сlient,
            #         contract_sum=contract_sum,
            #         contract_new=contract_new
            #     ) 

    # latest_question_list = Client.objects.all().order_by("-id")
    # context = {
    #     "latest_question_list":latest_question_list, 
    #     }
    # return render(request, "client/index.html", context)

# class ClientsListView(generic.ListView):
#     model = Client 
    
# #    class ClientsListView(TemplateView): 
# class ClientsListView(TemplateView):
#     def client_list(self, request, *args, **kwargs):
#         client_lists = self.objects.all().order_by("-id")
#         context = {
#             "client_lists":client_lists, 
#             "request_url": self.request.path,
#             }
#         return render(request, "client_list.html", context)