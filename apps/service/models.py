from django.db import models
from apps.client.models import AdditionalContract, Client, Contract
from django.utils import timezone
from apps.employee.models import Employee

from apps.operation.models import OperationEntry, OperationOut

# Create your models here.
# created_timestamp = models.DateTimeField(default=timezone.now)


# конкретная услуга клиента
class ServiceClient(models.Model):
    SERVICES_NAME = (
        ("ADV", "ADV"),
        ("SEO", "SEO"),
        ("SUP", "SUP"),
        ("DEV", "DEV"),
        ("SMM", "SMM"),
        ("NONE", "---"),
    )
    services_name = models.CharField(
        max_length=4, choices=SERVICES_NAME, default="NONE"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
    )

    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    # adv_all_sum = models.PositiveIntegerField("",default="0")

    def __str__(self):
        return str(self.services_name)


# ежемесячный счет по услуге
class ServicesMonthlyBill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True)
    service = models.ForeignKey(
        ServiceClient, on_delete=models.PROTECT, blank=True, null=True
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, blank=True, null=True
    )
    additional_contract = models.ForeignKey(
        AdditionalContract, on_delete=models.PROTECT, blank=True, null=True
    )

    subcontract = models.ForeignKey(
        "SubcontractMonth", on_delete=models.SET_NULL, blank=True, null=True
    )
    adv_all_sum = models.PositiveIntegerField("", default="0")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    check_entry = models.ForeignKey(
        OperationEntry,
        verbose_name="Проверка оплаты",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    comment = models.TextField("Комментарий", blank=True, null=True)


# # надо отключить модель
# class SubcontractAll(models.Model):
#     service_client = models.ForeignKey(
#         ServiceClient, on_delete=models.CASCADE, blank=True, null=True
#     )

#     seosub_people = models.CharField(max_length=200, blank=True, null=True)
#     seosub_sum = models.PositiveIntegerField(default="0")
#     seosub_people_other = models.CharField(max_length=200, blank=True, null=True)
#     seosub_sum_other = models.PositiveIntegerField(default="0")

#     drvsub_people = models.CharField(max_length=200, blank=True, null=True)
#     drvsub_sum = models.PositiveIntegerField(default="0")

#     designersub_people = models.CharField(max_length=200, blank=True, null=True)
#     designersub_sum = models.PositiveIntegerField(default="0")

#     created_timestamp = models.DateTimeField(
#         auto_now_add=True, verbose_name="Дата добавления"
#     )


# # надо отключить модель
# class SubcontractADV(models.Model):
#     service_client = models.ForeignKey(
#         ServiceClient, on_delete=models.CASCADE, blank=True, null=True
#     )
#     ADV = (
#         ("YANDEX", "Яндекс Директ"),
#         ("MAIL", "Таргет Mail.ru/VK"),
#         ("GOOGLE", "Google Adwords"),
#         ("OTHER", "ДРУГОЕ"),
#         ("NONE", "---"),
#     )

#     adv_name = models.CharField(max_length=10, choices=ADV, default="NONE")
#     adv_sum = models.PositiveIntegerField(default="0")
#     created_timestamp = models.DateTimeField(
#         auto_now_add=True, verbose_name="Дата добавления"
#     )


# субподряд для ежемесячного счета
class SubcontractMonth(models.Model):
    people = models.ForeignKey(
        Employee,
        verbose_name="Сотрудник",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    adv = models.ForeignKey(
        "Adv",
        verbose_name="Рекламная площадка",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    other = models.ForeignKey(
        "SubcontractOther",
        verbose_name="Рекламная площадка",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    # Запланированные траты
    amount = models.PositiveIntegerField("сумма субподряд", default="0")
    percent = models.PositiveIntegerField("процент для исполнителя", default="0")

    # фактические оплаты
    check_entry = models.ForeignKey(
        OperationOut,
        verbose_name="Проверка оплаты",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


#  Субподряд площадки
class Adv(models.Model):
    name = models.CharField("название площадки", max_length=200, blank=True, null=True)


class SubcontractOther(models.Model):
    name = models.CharField(
        "название субподряда", max_length=200, blank=True, null=True
    )


