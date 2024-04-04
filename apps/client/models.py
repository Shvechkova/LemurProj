from django.db import models
from django.urls import reverse

from apps.employee.models import Employee


# from apps.service.models import ServiceClient


# Create your models here.


class Client(models.Model):
    client_name = models.CharField("имя клиента", max_length=200)
    manager = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name="Менеджер",
        blank=True,
        null=True,
    )
     
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    # def __str__(self):
    #     return self.client_name


# Основной контракт
class Contract(models.Model):
    contract_number = models.CharField("название номер контракта", max_length=200)
    contract_sum = models.PositiveIntegerField("сумма контракта", default="0")
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент", blank=True, null=True
    )
    date_start = models.DateField("Дата начала действия", blank=True, null=True)
    # date_end = models.DateField("Дата окончания", blank=True, null=True)
    service = models.ForeignKey(
        "service.Service",
        on_delete=models.PROTECT,
        verbose_name="Конкретная услуга клиента",
        blank=True,
        null=True,
    )
    created_timestamp = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name="ответсвенный контракта",
        blank=True,
        null=True,
    )
    
    # def get_contracts_client(self,client_id):
    #     contract_in_client = self.objects.filter(client=client_id)
    #     return contract_in_client
    class Meta:
        verbose_name = "Контракт главный"
        verbose_name_plural = "Контракты главные"

    # def __str__(self):
    #     return self.contract_number



# # дополнительный контракт(к основному)
# class AdditionalContract(models.Model):
#     contract_number = models.CharField("название номер контракта", max_length=200)
#     client = models.ForeignKey(
#         Client, on_delete=models.PROTECT, verbose_name="Клиент", blank=True, null=True
#     )
#     # services = models.ForeignKey(
#     #      Service, on_delete=models.PROTECT,  verbose_name="Конкретная услуга клиента",blank=True, null=True
#     # )
#     service = models.ForeignKey(
#         "service.Service",
#         on_delete=models.PROTECT,
#         verbose_name="Конкретная услуга клиента",
#         blank=True,
#         null=True,
#     )
#     main_contract = models.ForeignKey(
#         Contract,
#         on_delete=models.SET_NULL,
#         verbose_name="главный контракт",
#         blank=True,
#         null=True,
#     )
#     contract_sum = models.PositiveIntegerField("сумма контракта", default="0")
#     diff_sum = models.PositiveIntegerField("сумма контракта", default="0")
#     created_timestamp = models.DateTimeField(
#         auto_now_add=True, verbose_name="Дата добавления"
#     )
#     adv_all_sum = models.PositiveIntegerField("", default="0")


