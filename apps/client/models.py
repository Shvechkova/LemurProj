from django.db import models
from django.urls import reverse


# from apps.service.models import ServiceClient


# Create your models here.


class Client(models.Model):
    client_name = models.CharField(max_length=200)

    def __str__(self):
        return self.client_name

# Основной контракт
class Contract(models.Model):
    contract_number = models.CharField("название номер контракта", max_length=200)
    contract_sum = models.PositiveIntegerField("сумма контракта", default="0")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент", blank=True, null=True)
    date_start = models.DateField("Дата начала действия", blank=True, null=True)
    date_end = models.DateField("Дата окончания", blank=True, null=True)
    service = models.ForeignKey(
        "service.ServiceClient", on_delete=models.PROTECT, verbose_name="Конкретная услуга клиента", blank=True, null=True
    )
    created_timestamp = models.DateTimeField("Дата добавления",
        auto_now_add=True, 
    )



# дополнительный контракт(к основному)
class AdditionalContract(models.Model):
    contract_number = models.CharField("название номер контракта",max_length=200)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент", blank=True, null=True)
    service = models.ForeignKey(
        "service.ServiceClient", on_delete=models.PROTECT,  verbose_name="Конкретная услуга клиента",blank=True, null=True
    )
    main_contract = models.ForeignKey(
        Contract, on_delete=models.SET_NULL, verbose_name="главный контракт", blank=True, null=True
    )
    contract_sum = models.PositiveIntegerField("сумма контракта", default="0")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
