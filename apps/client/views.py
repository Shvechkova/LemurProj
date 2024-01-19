# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.service.models import ServiceClient
from .models import Client, Contract
from .forms import (ClientNew, NewServiceClient)

# Create your views here.


def index(request):
    if request.method == "POST" and "window" in request.POST:
        if request.POST["window"] == "client_add":
            form = ClientNew(request.POST)
            if form.is_valid():
                client_name = form.cleaned_data["client_name"]
                client_new = Client.objects.create(
                    client_name=client_name
                )
                return HttpResponseRedirect(request.path)
        
        if request.POST["window"] == "service_add":
            form = NewServiceClient(request.POST)
            service_list = ServiceClient.objects.all()
            context = {
                "service_list":service_list
                }
            return render(request, "client/index.html", context)

    latest_question_list = Client.objects.all().order_by("-id")
    # service_list = ServiceClient.objects.all()
   
    # service_add = ServiceClient.services_name
    context = {
        "latest_question_list":latest_question_list, 
        # "service_list":service_list
        }
    return render(request, "client/index.html", context)
