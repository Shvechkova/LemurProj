from django.db import models
from apps.client.models import AdditionalContract, Client, Contract
from django.utils import timezone
from apps.employee.models import Employee
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth


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
            Sum("amount",default=0)
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

        operation_entry = OperationEntry.objects.filter(monthly_bill=self.id).values("monthly_bill","bank").annotate(total_amount=Sum("amount", default=0))
        return operation_entry
    
    def diff_sum_adv(self):
        this_contract = AdditionalContract.objects.get(servicesmonthlybill=self.id)
        diff = this_contract.contract_sum -this_contract.adv_all_sum
        
        return diff
    
    def sum_other_subcontr(self):
        sub_sum = SubcontractMonth.objects.filter(
        month_bill=self.id, other__isnull=False).aggregate(Sum("amount", default=0))
        # sum_actual = sub_sum.get("amount__sum")
        return sub_sum  
    
    def sum_real_subcontract(self):
        suncontr_month = SubcontractMonth.objects.filter(
        month_bill=self.id,).aggregate(Sum("amount", default=0))
        return suncontr_month  
    
    def sum_operation_out_subcontract(self):
        from apps.operation.models import OperationOut
        suncontr_out = OperationOut.objects.filter(
        suborder__month_bill=self.id,).aggregate(Sum("sum", default=0))
       
        return suncontr_out 
    
    def diff_subcontr_out(self):
        suncontr_month = SubcontractMonth.objects.filter(
        month_bill=self.id,).aggregate(Sum("amount", default=0))
        
        from apps.operation.models import OperationOut
        suncontr_out = OperationOut.objects.filter(
        suborder__month_bill=self.id,).aggregate(Sum("sum", default=0))
        
        # for c in suncontr_month:
        #     print(c) suncontr_out['sum__sum']
        diff_subs = suncontr_month['amount__sum'] - suncontr_out['sum__sum']
        
        return diff_subs 
       

    @classmethod
    def get_total_income(cls, category_service):
        total_income = (
            cls.objects.filter(service=category_service)
            .annotate(month=TruncMonth("created_timestamp"))
            .values("month")
            .annotate(total_amount=Sum("additional_contract__contract_sum"))
        )

        return total_income


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
    
    
#  Субподряд площадки
class Adv(models.Model):
    name = models.CharField("название площадки", max_length=200, blank=True, null=True)


class SubcontractOther(models.Model):
    name = models.CharField(
        "название субподряда", max_length=200, blank=True, null=True
    )
