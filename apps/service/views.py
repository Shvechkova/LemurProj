

from django.shortcuts import render
from apps.client.models import Contract

from apps.service.models import ServiceClient


def index(request):
    # if request.method == "POST" :
    #     form = ClientNew(data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('clients:index'))
    # else:
    #     form = ClientNew()

    
    
    # client_list = Client.objects.all()
    title='Услуги'
    context = {
        'title': title,
        # 'client_list': client_list,
        # 'form': form,
      
    }
    return render(request, 'service/service.html', context)

def serviced(request, slug):
    service_client = ServiceClient.objects.filter(services_name=slug)
    actual_contract =  Contract.objects.all()
    title='Одна услуга'
    context = {
        'title': slug,
        'service_client': service_client,
        'actual_contract': actual_contract,
        # 'client_list': client_list,
        # 'form': form,
    }
    
    return render(request, 'service/one_servis.html', context)