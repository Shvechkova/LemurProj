from django.db import models
from apps.client.models import Client, Contract
from django.utils import timezone
# Create your models here.
# created_timestamp = models.DateTimeField(default=timezone.now)

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
    # month = models.CharField( max_length=4, choices=MONTH, default="NONE")
    client = models.ForeignKey(Client, on_delete=models.CASCADE,)
    # contract = models.ForeignKey(Contract,  on_delete=models.CASCADE,blank=True, null=True)
    # contract_sum = models.PositiveIntegerField(default="0")
    account = models.CharField( max_length=4, choices=ACCOUNT, default="NONE")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    

    def __str__(self):
        return str(self.services_name)
        
class SubcontractAll(models.Model):
    service_client = models.ForeignKey(ServiceClient, on_delete=models.CASCADE,blank=True, null=True)
    seosub_people = models.CharField(max_length=200,blank=True, null=True)
    seosub_sum = models.PositiveIntegerField(default="0") 
    seosub_people_other=models.CharField(max_length=200,blank=True, null=True)
    seosub_sum_other=models.PositiveIntegerField(default="0") 
    drvsub_people = models.CharField(max_length=200,blank=True, null=True)
    drvsub_sum = models.PositiveIntegerField(default="0")
    designersub_people = models.CharField(max_length=200,blank=True, null=True)
    designersub_sum = models.PositiveIntegerField(default="0")
    adv_all_sum = models.PositiveIntegerField(default="0")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    
    
class SubcontractADV(models.Model): 
    service_client = models.ForeignKey(ServiceClient, on_delete=models.CASCADE,blank=True, null=True) 
    ADV = (
        ("YANDEX", "Яндекс Директ"),
        ("MAIL", "Таргет Mail.ru/VK"),
        ("GOOGLE", "Google Adwords"),
        ("OTHER", "ДРУГОЕ"),
        ("NONE", "---"),
    ) 
     
    adv_name = models.CharField(
        max_length=10, choices=ADV, default="NONE")
    adv_sum = models.PositiveIntegerField(default="0")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    