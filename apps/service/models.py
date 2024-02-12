from django.db import models
from apps.client.models import AdditionalContract, Client, Contract
from django.utils import timezone
from apps.employee.models import Employee
from django.db.models import Count, Sum


# from apps.operation.models import OperationEntry, OperationOut


# Create your models here.
# created_timestamp = models.DateTimeField(default=timezone.now)
class Service(models.Model):
    name = models.CharField("Категории услуг", max_length=150, blank=True, null=True)


# конкретная услуга клиента
class ServiceClient(models.Model):
    client = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        blank=True,
        null=True,
    )
    service = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Клиент",
        blank=True,
        null=True,
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
        Service, on_delete=models.PROTECT, blank=True, null=True
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

    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    def get_all_sum_entry_operation(self):
        from apps.operation.models import OperationEntry

        contract_sum = self.additional_contract.contract_sum

        operation_entry = OperationEntry.objects.filter(monthly_bill=self.id).aggregate(
            Sum("amount")
        )

        if operation_entry["amount__sum"] != None:
            result = contract_sum - operation_entry["amount__sum"]
            if result != 0:
                obj = {
                    "result": result,
                    "operation_amount": operation_entry["amount__sum"],
                }
                return obj
            return contract_sum
        else:
            return "0"
        
    def get_sum_bank_operaton_entry(self):
        from apps.operation.models import OperationEntry

        operation_entry = OperationEntry.objects.filter(monthly_bill=self.id).values('bank').annotate(total_amount=Sum('amount'))
        print(operation_entry)
        # obj = {}
        for operation in operation_entry:
            obj = {
                    "bank": operation["bank"],
                    "operation_amount": operation["total_amount"],
                }
            return
           
            
            
        
     
        return "0"    


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
        verbose_name="Тип субподряда",
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
    month_bill = models.ForeignKey(
        ServicesMonthlyBill, on_delete=models.SET_NULL, blank=True, null=True
    )

    # фактические оплаты
    # check_entry = models.ForeignKey(
    #     OperationOut,
    #     verbose_name="Проверка оплаты",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )


#  Субподряд площадки
class Adv(models.Model):
    name = models.CharField("название площадки", max_length=200, blank=True, null=True)


class SubcontractOther(models.Model):
    name = models.CharField(
        "название субподряда", max_length=200, blank=True, null=True
    )
