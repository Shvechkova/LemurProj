from django.db import models
from django.urls import reverse



# from apps.service.models import ServiceClient




# Create your models here.

class Client(models.Model):
    client_name = models.CharField(max_length=200)
    # contract = models.ForeignKey(to=Contract,  on_delete=models.CASCADE, blank=True,
    #     null=True)
    
    def __str__(self):
        return self.client_name
    
   
    
    
class Contract(models.Model):
    contract_number = models.CharField(max_length=200)
    contract_sum = models.PositiveIntegerField(default="0") 
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True,null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    service = models.ForeignKey('service.ServiceClient',  on_delete=models.CASCADE, blank=True,null=True)   
    
  