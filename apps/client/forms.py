from django import forms
from .models import Client,Contract
from apps.service.models import ServiceClient

class ClientNew(forms.ModelForm):
    class Meta:
        model = Client
        # fields = ('client_name',)
        fields = ('__all__')
        
class NewServiceClient(forms.ModelForm):
    class Meta:
        model = ServiceClient
        fields = ['services_name', 'client'] 
        # fields = ('__all__')      
        
# class AddService(forms.Form):
#     client_id = forms.IntegerField()  
    
class AddContract(forms.ModelForm):
    contract_number = forms.CharField()
    contract_sum = forms.IntegerField()
    date_start = forms.DateField()
    date_end = forms.DateField()
    
    
    class Meta:
         model = Contract
         fields = ('__all__')
                           