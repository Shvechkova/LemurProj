from django import forms
from .models import Client
from apps.service.models import ServiceClient

class ClientNew(forms.ModelForm):
    class Meta:
        model = Client
        # fields = ('client_name',)
        fields = ('__all__')
        
class NewServiceClient(forms.ModelForm):
    class Meta:
        model = ServiceClient
        # fields = ['services_name', 'client'] 
        fields = ('__all__')      