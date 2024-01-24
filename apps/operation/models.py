from django.db import models

from apps.client.models import Contract

# from apps.bank.models import Bank


# Create your models here.

class OperationEntry(models.Model):
    
    # bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True,null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    sum = models.PositiveIntegerField(default="0")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True,null=True) 
    comment=models.TextField(blank=True,null=True)

class OperationOut(models.Model):
    # bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True,null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    sum = models.PositiveIntegerField(default="0") 

