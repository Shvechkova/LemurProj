from django.db import models
from apps.client.models import Client, Contract
# Create your models here.


# class TypeService(models.Model):
#     # name = models.CharField(max_length=200)


# class Service(models.Model):
#     SERVICES_NAME = (
#         ("ADV", "ADV"),
#         ("SEO", "SEO"),
#         ("SUP", "SUP"),
#         ("DEV", "DEV"),
#         ("SMM", "SMM"),
#     )
   
#     services_name = models.CharField(
#         max_length=3, choices=SERVICES_NAME, default=""
#     )


class ServiceClient(models.Model):
    SERVICES_NAME = (
        ("ADV", "ADV"),
        ("SEO", "SEO"),
        ("SUP", "SUP"),
        ("DEV", "DEV"),
        ("SMM", "SMM"),
        ("NONE", "NONE"),
    )
    
    MONTH = (
        ("1", "Январь"),
        ("2", "Февраль"),
        ("NONE", "NONE"),
        
    )
    
    ACCOUNT = (
        ("1", "OOO"),
        ("2", "ИП"),
        ("2", "Нал"),
        ("NONE", "NONE"),
        
    )
    
    services_name = models.CharField(
        max_length=4, choices=SERVICES_NAME, default="NONE")
    month = models.CharField( max_length=4, choices=MONTH, default="NONE")
    client = models.ForeignKey(Client, on_delete=models.CASCADE,)
    contract = models.ForeignKey(Contract,  on_delete=models.CASCADE,blank=True, null=True)
    contract_sum = models.PositiveIntegerField(default="0")
    account = models.CharField( max_length=4, choices=ACCOUNT, default="NONE")
       
    
    
    def __str__(self):
        return str(self.services_name)
    
     
  
    # def save(self, *args, **kwargs):
    #     return super(ServiceClient, self).save(*args, **kwargs)
        
        
# class Subcontract(models.Model):
                  