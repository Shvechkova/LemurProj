from django.db import models


# Create your models here.

    
class Contract(models.Model):
    contract_number = models.CharField(max_length=200)
    contract_sum = models.PositiveIntegerField(default="0")
    
    
class Client(models.Model):
    client_name = models.CharField(max_length=200)
    contract = models.ForeignKey(Contract,  on_delete=models.CASCADE, blank=True,
        null=True)
    
    def __str__(self):
        return self.client_name
    
  