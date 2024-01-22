# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView

from apps.service.models import ServiceClient
from .models import Client, Contract
from .forms import (ClientNew, NewServiceClient, AddContract)

# Create your views here.


def clients(request):
    if request.method == "POST" :
        form = ClientNew(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clients:index'))
    else:
        form = ClientNew()

    
    
    client_list = Client.objects.all()
    title='Клиенты'
    context = {
        'title': title,
        'client_list': client_list,
        'form': form,
      
    }
    return render(request, 'client/index.html', context)


def client(request,client_id):
    if request.method == "POST" and "window" in request.POST:
        if request.POST["window"] == "service":
            form = NewServiceClient(request.POST)
            if form.is_valid():
                client =  form.cleaned_data["client"]
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
        'client': client,
        'client_service': client_service,
        # "services_name": NewServiceClient,
        "form": form,
    }
    return render(request, 'client/client.html', context)
   
def addContract(request,client_id,slug):
    client = Client.objects.get(id=client_id)
    service = ServiceClient.objects.get(client=client_id,services_name=slug)
    # service_form = ServiceClient.objects.get(client=client_id)
    
    if request.method == "POST":
        form = AddContract(request.POST)
        if form.is_valid():
            contract_number =  form.cleaned_data["contract_number"] 
            contract_sum =  form.cleaned_data["contract_sum"] 
            date_start =  form.cleaned_data["date_start"] 
            date_end =  form.cleaned_data["date_end"] 
            service =  service
            client =  client
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

    # client = Client.objects.get(id=client_id)
    # service = ServiceClient.objects.get(client=client_id)
    contract = Contract.objects.filter(client=client_id)
    form = AddContract()
    context = {
        'client': client, 
        'service': service,
        'contract': contract,
        'form': form,  
       
    }
    return render(request, 'client/add_contract.html', context)