from django.db import models
from apps.client.models import  Client, Contract
from django.utils import timezone
from apps.employee.models import Employee
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Q
from django.core.cache import cache


# created_timestamp = models.DateTimeField(default=timezone.now)
class Service(models.Model):
    name = models.CharField(
        "Категории услуг", max_length=150, blank=True, null=True)


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
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, blank=True, null=True)
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, blank=True, null=True
    )
    contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, blank=True, null=True
    )
    # additional_contract = models.ForeignKey(
    #     AdditionalContract, on_delete=models.PROTECT, blank=True, null=True
    # )

    subcontract = models.ForeignKey(
        "SubcontractMonth", on_delete=models.SET_NULL, blank=True, null=True
    )

    created_timestamp = models.DateField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    # data = models.DateTimeField(default=timezone.now)

    contract_number = models.CharField(
        "название номер контракта", max_length=200, default=None
    )

    contract_sum = models.PositiveIntegerField("сумма контракта", default="0")

    adv_all_sum = models.PositiveIntegerField(
        "сумма ведения для адв", default=None, blank=True, null=True)

    diff_sum = models.PositiveIntegerField(
        "сумма для распределения по скбподряду адв", default="0"
    )

    chekin_sum_entrees = models.BooleanField(
        "чекин получения полной оплаты от клиента", default=False
    )

    chekin_sum_adv = models.BooleanField(
        "чекин оплаты всех субподрядов", default=False)

    chekin_add_subcontr = models.BooleanField(
        "чекин есть ли распределение денег по субподрядам", default=False
    )
    # все операции по счету 
    def get_operation(self):
        from apps.operation.models import Operation
        operation = Operation.objects.filter(monthly_bill=self.id).select_related(
            "bank","suborder"
        )
      
        sum_all_operation_entry = 0
        sum_operation_entry_bank1 = 0
        sum_operation_entry_bank2 = 0
        sum_operation_entry_bank3 = 0
        comment_operation_entry_bank1 = []
        comment_operation_entry_bank2 = []
        comment_operation_entry_bank3 = []
        id_operation_entry = ""

        for oper in operation:  
           
            if oper.type_operation == "entry":
              
                sum_all_operation_entry += oper.amount
                id_operation_entry = id_operation_entry + str(oper.id) + "-"

                if oper.bank.id == 1:
                    sum_operation_entry_bank1 += oper.amount
                    if oper.comment:
                        comment = {
                            "data": oper.data,
                            "sum":oper.amount,
                            "comment":oper.comment,
                            #  "name":oper.suborder.name,
                        }
                        comment_operation_entry_bank1.append(comment)

                elif oper.bank.id == 2:
                    sum_operation_entry_bank2 += oper.amount
                    if oper.comment:
                        comment = {
                            "data": oper.data,
                            "sum":oper.amount,
                            "comment":oper.comment,
                            #  "name":oper.suborder.name,
                        }
                        comment_operation_entry_bank2.append(comment)
                    
                elif oper.bank.id == 3:
                    sum_operation_entry_bank3 += oper.amount
                    if oper.comment:
                        comment = {
                            "data": oper.data,
                            "sum":oper.amount,
                            "comment":oper.comment,
                            #  "name":oper.suborder.other.name,
                        }
                        comment_operation_entry_bank3.append(comment)

        sum_all_operation_out = 0
        sum_operation_out_bank1 = 0
        sum_operation_out_bank2 = 0
        sum_operation_out_bank3 = 0
        comment_operation_out_bank1 = []
        comment_operation_out_bank2 = []
        comment_operation_out_bank3 = []
        id_operation_out = ""

        for oper_out in operation:
            if oper_out.type_operation == "out":
                # print(oper.suborder.other.name)
                sum_all_operation_out += oper_out.amount
                id_operation_out = id_operation_out + str(oper_out.id) + "-"
                if oper_out.bank.id == 1:
                    sum_operation_out_bank1 += oper_out.amount
                    if oper_out.comment:
                        comment = {
                            "data": oper_out.data,
                            "sum":oper_out.amount,
                            "comment":oper_out.comment,
                            # "name":oper_out.suborder.other.name,
                        }
                        comment_operation_out_bank1.append(comment)

                elif oper_out.bank.id == 2:
                    sum_operation_out_bank2 += oper_out.amount
                    if oper_out.comment:
                        comment = {
                            "data": oper_out.data,
                            "sum":oper_out.amount,
                            "comment":oper_out.comment,
                            # "name":oper_out.suborder.other.name,
                        }
                        comment_operation_out_bank2.append(comment)
                elif oper_out.bank.id == 3:
                    sum_operation_out_bank3 += oper_out.amount
                    if oper_out.comment:
                        comment = {
                            "data": oper_out.data,
                            "sum":oper_out.amount,
                            "comment":oper_out.comment,
                            # "name":oper_out.suborder.other.name,
                        }
                        comment_operation_out_bank3.append(comment)

        diff_operation_entry = self.contract_sum - sum_all_operation_entry

        if self.adv_all_sum == 0:
            suborders = SubcontractMonth.objects.filter(month_bill=self.id, other__isnull=False).select_related(
                "other").aggregate(total_amount=Sum('amount', default=0))

            diff_operation_out = suborders['total_amount'] - \
                sum_all_operation_out

        else:
            diff_operation_out = self.diff_sum - sum_all_operation_out

        obj = [
            {
                "operation_entry_all": sum_all_operation_entry,
                "diff_operation_entry": diff_operation_entry,
                "id_operation_entry": id_operation_entry,
                "operation_entry_bank1": sum_operation_entry_bank1,
                "operation_entry_bank2": sum_operation_entry_bank2,
                "operation_entry_bank3": sum_operation_entry_bank3,
                "comment_entry_bank1": comment_operation_entry_bank1,
                "comment_entry_bank2": comment_operation_entry_bank2,
                "comment_entry_bank3": comment_operation_entry_bank3,
                "operation_out_all": sum_all_operation_out,
                "diff_operation_out": diff_operation_out,
                "id_operation_out": id_operation_out,
                "operation_out_bank1": sum_operation_out_bank1,
                "operation_out_bank2": sum_operation_out_bank2,
                "operation_out_bank3": sum_operation_out_bank3,
                "comment_out_bank1": comment_operation_out_bank1,
                "comment_out_bank2": comment_operation_out_bank2,
                "comment_out_bank3": comment_operation_out_bank3,
            }
        ]
       
        return obj
   
    # субподряды адв
    def suborders_adv(self):
        suborders = SubcontractMonth.objects.filter(
            month_bill=self.id, adv__isnull=False
        ).select_related("adv").values('id', 'adv__name', 'amount', 'adv_id')
        
        def loc_mem_cache(key, function, timeout=300):
            cache_data = cache.get(key)
            if not cache_data:
                cache_data = function()
                cache.set(key, cache_data, timeout)
            return cache_data
        
        def suborders_name_cache():
            def cache_function():
                suborders_name = Adv.objects.all()
                return suborders_name

            return loc_mem_cache('suborders_name', cache_function, 500)

        suborders_name = suborders_name_cache()
        
        # suborders_name = Adv.objects.all()
        obj = []

        for subs_item in suborders_name:
            name = {
                "name_adv": subs_item.name,
                "id_adv": subs_item.id,
                "id_subs": 0,
                "amount": 0,
            }
            obj.append(name)

        for x in range(len(obj)):
            for y in range(len(suborders)):
                if obj[x]['id_adv'] == suborders[y]['adv_id']:
                    obj[x]['id_subs'] = suborders[y]['id']
                    obj[x]['amount'] = suborders[y]['amount']

        return (obj)
    # субподряды другое для адв
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

        return (obj)
    # субподряд для категори не адв
    def suborders_other_no_adv(self):
        suborders = SubcontractMonth.objects.filter(
            month_bill=self.id, other__isnull=False
        ).select_related("other")
        suborders_name = SubcontractOther.objects.all()

        obj = []
    
        for subs_item in suborders_name:
            name = {
                "name": subs_item.name,
                "id_other": 0,
                "id_amount": 0,

            }
            obj.append(name)

        count_categoru = len(obj) + 1

        total_amount = 0
        id_subs = ""
        i = -1
        obj_new = [{"name_other": 0, "id_other": 0,
                    "id_amount": 0}] * count_categoru

        for subs_item in suborders:
            total_amount += subs_item.amount
            id_subs = id_subs + str(subs_item.id) + "-"
            i += 1
            name = {

                "name_other": subs_item.other.name,
                "id_other": subs_item.id,
                "id_amount": subs_item.amount,

            }
            obj_new[i] = name

        for x in range(len(obj)):
            for y in range(len(obj_new)):
                if obj[x]['name'] == obj_new[y]['name_other']:
                    obj[x].update(obj_new[y])

        total = {
            "total_amount": total_amount,
            "id_subs": id_subs,
        }
        obj.insert(0, total)
        
        return (obj)

    # def suborders_other_no_adv_total(self):
    #     suborders = SubcontractMonth.objects.filter(
    #         month_bill=self.id, other__isnull=False
    #     ).select_related("other")

    #     obj = []
    #     total_amount = 0
    #     id_subs = ""
    #     for subs_item in suborders:
    #         total_amount += subs_item.amount
    #         id_subs = id_subs + str(subs_item.id) + "-"

    #     total = {
    #         "total_amount": total_amount,
    #         "id_subs": id_subs,
    #     }
    #     obj.insert(0, total)

    #     return (obj)


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

    created_timestamp = models.DateField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    # Запланированные траты
    amount = models.PositiveIntegerField("сумма субподряд", default="0")
    percent = models.PositiveIntegerField(
        "процент для исполнителя", default="0")
    month_bill = models.ForeignKey(
        ServicesMonthlyBill, on_delete=models.CASCADE, blank=True, null=True
    )

    # chekin_sum_out =  models.BooleanField(default=False)

#  Субподряд площадки


class Adv(models.Model):
    name = models.CharField("название площадки",
                            max_length=200, blank=True, null=True)


class SubcontractOther(models.Model):
    name = models.CharField(
        "название субподряда", max_length=200, blank=True, null=True
    )
