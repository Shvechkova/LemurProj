from django.db import models
from apps.client.models import AdditionalContract, Client, Contract
from django.utils import timezone
from apps.employee.models import Employee
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Q


# from apps.operation.models import OperationEntry, OperationOut


# Create your models here.f
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

    contract_number = models.CharField(
        "название номер контракта", max_length=200, default=None
    )

    contract_sum = models.PositiveIntegerField("сумма контракта", default="0")

    adv_all_sum = models.PositiveIntegerField("сумма ведения для адв", default="0")

    diff_sum = models.PositiveIntegerField(
        "сумма для распределения по скбподряду адв", default="0"
    )

    chekin_sum_entrees = models.BooleanField(
        "чекин получения полной оплаты от клиента", default=False
    )

    chekin_sum_adv = models.BooleanField("чекин оплаты всех субподрядов", default=False)

    chekin_add_subcontr = models.BooleanField(
        "чекин есть ли распределение денег по субподрядам", default=False
    )

    # def get_all_sum_entry_operation(self):
    #     from apps.operation.models import OperationEntry

    #     contract_sum = self.additional_contract.contract_sum

    #     operation_entry = OperationEntry.objects.filter(monthly_bill=self.id).aggregate(
    #         Sum("amount", default=0)
    #     )

    #     if operation_entry["amount__sum"] != None:
    #         result = contract_sum - operation_entry["amount__sum"]
    #         if result != 0:
    #             obj = {
    #                 "result": result,
    #                 "operation_amount": operation_entry["amount__sum"],
    #             }
    #             return obj
    #         return contract_sum
    #     else:
    #         return "0"

    # суммы по операциям прихода денег банки
    # def get_sum_bank_operaton_entry_bank_one(self):
    #     from apps.operation.models import OperationEntry

    #     operation_entry = (
    #         OperationEntry.objects.filter(monthly_bill=self.id, bank=1)
    #         .values("bank")
    #         .annotate(total_amount=Sum("amount", default=0))
    #     )
    #     return operation_entry

    # def get_sum_bank_operaton_entry_bank_two(self):
    #     from apps.operation.models import OperationEntry

    #     operation_entry = (
    #         OperationEntry.objects.filter(monthly_bill=self.id, bank=2)
    #         .values("bank")
    #         .annotate(total_amount=Sum("amount", default=0))
    #     )
    #     return operation_entry

    # def get_sum_bank_operaton_entry_bank_three(self):
    #     from apps.operation.models import OperationEntry

    #     operation_entry = (
    #         OperationEntry.objects.filter(monthly_bill=self.id, bank=3)
    #         .values("bank")
    #         .annotate(total_amount=Sum("amount", default=0))
    #     )
    #     return operation_entry

    # def diff_sum_adv(self):
    #     this_contract = AdditionalContract.objects.get(servicesmonthlybill=self.id)
    #     diff = this_contract.contract_sum - this_contract.adv_all_sum

    #     return diff

    # def sum_other_subcontr(self):
    #     sub_sum = SubcontractMonth.objects.filter(
    #         month_bill=self.id, other__isnull=False
    #     ).aggregate(Sum("amount", default=0))
    #     # sum_actual = sub_sum.get("amount__sum")
    #     return sub_sum

    # def sum_real_subcontract(self):
    #     suncontr_month = SubcontractMonth.objects.filter(
    #         month_bill=self.id,
    #     ).aggregate(Sum("amount", default=0))
    #     return suncontr_month

    # def sum_operation_out_subcontract(self):
    #     from apps.operation.models import OperationOut

    #     suncontr_out = OperationOut.objects.filter(
    #         suborder__month_bill=self.id,
    #     ).aggregate(Sum("sum", default=0))

    #     return suncontr_out

    # def diff_subcontr_out(self):
    #     suncontr_month = SubcontractMonth.objects.filter(
    #         month_bill=self.id,
    #     ).aggregate(Sum("amount", default=0))

    #     from apps.operation.models import OperationOut

    #     suncontr_out = OperationOut.objects.filter(
    #         suborder__month_bill=self.id,
    #     ).aggregate(Sum("sum", default=0))

    #     diff_subs = suncontr_month["amount__sum"] - suncontr_out["sum__sum"]

    #     return diff_subs

    # def diff_subcontr_out_operation(self):
    #     this_contract = AdditionalContract.objects.get(servicesmonthlybill=self.id)

    #     # suncontr_month = SubcontractMonth.objects.filter(
    #     # month_bill=self.id,).aggregate(Sum("amount", default=0))

    #     from apps.operation.models import OperationOut

    #     suncontr_out = OperationOut.objects.filter(
    #         suborder__month_bill=self.id,
    #     ).aggregate(Sum("sum", default=0))

    #     diff_all_out_operation = this_contract.diff_sum - suncontr_out["sum__sum"]

    #     # obj = []
    #     direct = {
    #         "all_sum_adv": this_contract.diff_sum,
    #         "all_operation_sum_out": suncontr_out["sum__sum"],
    #         "diff_sum": diff_all_out_operation,
    #     }

    #     return direct

    # def get_sum_bank_operaton_out_bank(self):
    #     from apps.operation.models import OperationOut

    #     operation_out_bank = (
    #         OperationOut.objects.filter(suborder__month_bill=self.id)
    #         .values("bank")
    #         .annotate(total_amount=Sum("sum", default=0))
    #     )
    #     obj = [{"bank": 0, "sum": 0}] * 3

    #     for sum_bank in operation_out_bank:
    #         if sum_bank["bank"] == 1:
    #             bank1 = {
    #                 "bank": sum_bank["bank"],
    #                 "sum": sum_bank["total_amount"],
    #             }
    #             obj[0] = bank1
    #         if sum_bank["bank"] == 2:
    #             bank2 = {
    #                 "bank": sum_bank["bank"],
    #                 "sum": sum_bank["total_amount"],
    #             }
    #             obj[1] = bank2
    #         if sum_bank["bank"] == 3:
    #             bank3 = {
    #                 "bank": sum_bank["bank"],
    #                 "sum": sum_bank["total_amount"],
    #             }
    #             obj[3] = bank3

    #     count = len(obj)

    #     return obj

    def get_operation(self):
        from apps.operation.models import Operation

        operation = Operation.objects.filter(monthly_bill=self.id).select_related(
            "bank"
        )

        sum_all_operation_entry = 0
        sum_operation_entry_bank1 = 0
        sum_operation_entry_bank2 = 0
        sum_operation_entry_bank3 = 0
        id_operation_entry = ""

        for oper in operation:
            if oper.type_operation == "entry":
                sum_all_operation_entry += oper.amount
                id_operation_entry = id_operation_entry + str(oper.id) + "-"

                if oper.bank.id == 1:
                    sum_operation_entry_bank1 += oper.amount

                elif oper.bank.id == 2:
                    sum_operation_entry_bank2 += oper.amount
                elif oper.bank.id == 3:
                    sum_operation_entry_bank3 += oper.amount

        sum_all_operation_out = 0
        sum_operation_out_bank1 = 0
        sum_operation_out_bank2 = 0
        sum_operation_out_bank3 = 0
        id_operation_out = ""

        for oper_out in operation:
            if oper_out.type_operation == "out":
                sum_all_operation_out += oper_out.amount
                id_operation_out = id_operation_out + str(oper_out.id) + "-"
                if oper_out.bank.id == 1:
                    sum_operation_out_bank1 += oper_out.amount

                elif oper_out.bank.id == 2:
                    sum_operation_out_bank2 += oper_out.amount
                elif oper_out.bank.id == 3:
                    sum_operation_out_bank3 += oper_out.amount

        diff_operation_entry = self.contract_sum - sum_all_operation_entry
        diff_operation_out = self.diff_sum - sum_all_operation_out

        obj = [
            {
                "operation_entry_all": sum_all_operation_entry,
                "diff_operation_entry": diff_operation_entry,
                "id_operation_entry": id_operation_entry,
                "operation_entry_bank1": sum_operation_entry_bank1,
                "operation_entry_bank2": sum_operation_entry_bank2,
                "operation_entry_bank3": sum_operation_entry_bank3,
                "operation_out_all": sum_all_operation_out,
                "diff_operation_out": diff_operation_out,
                "id_operation_out": id_operation_out,
                "operation_out_bank1": sum_operation_out_bank1,
                "operation_out_bank2": sum_operation_out_bank2,
                "operation_out_bank3": sum_operation_out_bank3,
            }
        ]

        return obj

    def suborders_adv(self):
        suborders = SubcontractMonth.objects.filter(
            month_bill=self.id, adv__isnull=False
        ).select_related("adv")
        suborders_name = Adv.objects.all()
        obj = []

        for subs_item in suborders_name:
            name = {
                "name_adv": subs_item.name,
                "id_adv": subs_item.id,
            }
            obj.append(name)
            
            
        count_categoru = len(obj)
        obj_new = [{"name-adv": 0, "id_subs": 0, "amount_subs": 0}] * count_categoru
        i = -1
        for nams, suborder in zip(obj, suborders):

            i += 1
            name = {
                "id_adv": nams["name_adv"],
                "name_adv": nams["id_adv"],
                "id_subs": suborder.id,
                "amount_subs": suborder.amount,
            }
            
            obj_new[i] = name
            # obj_new.append(name)

        count_item = len(obj_new)

        # suborders = SubcontractMonth.objects.filter(
        #     month_bill=self.id).select_related("adv","other")
        
        # suborders_name = Adv.objects.all()
        # obj = []
        # for subs_item in suborders_name:
        #     name = {
        #         "name_adv": subs_item.name,
        #         "id_adv": subs_item.id,
        #     }
        #     obj.append(name)

        # count_categoru = len(obj)
        
        # obj_new = [{"name-adv": 0, "id_subs": 0, "amount_subs": 0}] * count_categoru
        # i = -1
        # for sub in suborders:
        #     if sub.adv != None:
        #             i += 1
        #             name = {
        #                 "id_adv": nams["name_adv"],
        #                 "name_adv": nams["id_adv"],
        #                 "id_subs": suborder.id,
        #                 "amount_subs": suborder.amount,
        #             }
        #             obj_new[i] = name
        #             return (obj_new)  
              
        #     # if sub.other != None:
        #     #     suborders_name = SubcontractOther.objects.all()
               
        #     #     obj = []
        #     #     for subs_item in suborders_name:
        #     #         name = {
        #     #             "name_other": subs_item.name,
        #     #             "id_other": subs_item.id,
        #     #         }
        #     #         obj.append(name)
        #     #     print(obj)
        #     #     count_categoru = len(obj)
        #     #     obj_new = [{"name-other": 0, "id_subs": 0, "amount_subs": 0}] * count_categoru
        #     #     i = -1
        #     #     for nams, suborder in zip(obj, suborders):
        #     #         i += 1
        #     #         name = {
        #     #             "id_adv": nams["name_adv"],
        #     #             "name_adv": nams["id_adv"],
        #     #             "id_subs": suborder.id,
        #     #             "amount_subs": suborder.amount,
        #     #         }
        #     #         obj_new[i] = name
               
        return (obj_new)     
              
                
                
        
        
    
    def suborders_other(self):
        suborders = SubcontractMonth.objects.filter(
            month_bill=self.id, other__isnull=False
        ).select_related("other")

       
        obj = [] 
        total_amount = 0
        id_subs = ""
        for subs_item in suborders:
            total_amount += subs_item.amount
            id_subs = id_subs + str(subs_item.id) + "-"  
            name = {
                "id_cat_other": subs_item.other.name,
                "name_other": subs_item.other.name,
                "id_other": subs_item.id,
                "id_amount": subs_item.amount,
                
            }
            obj.append(name)
          
        total = {
                "total_amount": total_amount,
                "id_subs": id_subs,  
            }    
        obj.append(total)   
        print(obj)

        return (obj)

    # def get_sum_planning_adv(self):
    #     plannig_sum = SubcontractMonth.objects.filter(
    #         month_bill=self.id, adv__isnull=False
    #     )
    #     obj = []
    #     for plan in plannig_sum:
    #         if plan.adv_id == 1:
    #             direct = {
    #                 "id": plan.id,
    #                 "adv": plan.adv_id,
    #                 "sum": plan.amount,
    #             }
    #             obj.append(direct)
    #         if plan.adv_id == 2:
    #             target = {
    #                 "id": plan.id,
    #                 "adv": plan.adv_id,
    #                 "sum": plan.amount,
    #             }
    #             obj.append(target)

    #     count = len(obj)
    #     if count == 1:
    #         null_list = {
    #             "adv": 0,
    #             "0": 0,
    #             "0": 0,
    #         }
    #         obj.append(null_list)

    #     return obj

    # @classmethod
    # def get_total_income(cls, category_service):
    #     total_income = (
    #         cls.objects.filter(service=category_service)
    #         .annotate(month=TruncMonth("created_timestamp"))
    #         .values("month")
    #         .annotate(total_amount=Sum("additional_contract__contract_sum"))
    #     )

    #     return total_income

    # @classmethod
    # def get_total_income_adv(cls, category_service):
    #     total_adv = (
    #         cls.objects.filter(service=category_service)
    #         .annotate(month=TruncMonth("created_timestamp"))
    #         .values("month")
    #         .annotate(total_amount=Sum("additional_contract__adv_all_sum"))
    #     )

    #     return total_adv

    # @classmethod
    # def get_total_income_suborder(cls, category_service):
    #     total_sub_adv = (
    #         cls.objects.filter(service=category_service)
    #         .annotate(month=TruncMonth("created_timestamp"))
    #         .values("month")
    #         .annotate(total_amount=Sum("subcontractmonth__amount"))
    #     )

    #     return total_sub_adv

    # @classmethod
    # def get_total_operation_entry(cls, category_service):
    #     total_adv = (
    #         cls.objects.filter(service=category_service).annotate(month=TruncMonth(
    #     'created_timestamp')).values('month').annotate(total_amount=Sum('additional_contract__adv_all_sum'))
    #     )

    #     return total_adv


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
    # chekin_sum_out =  models.BooleanField(default=False)


#  Субподряд площадки
class Adv(models.Model):
    name = models.CharField("название площадки", max_length=200, blank=True, null=True)


class SubcontractOther(models.Model):
    name = models.CharField(
        "название субподряда", max_length=200, blank=True, null=True
    )
