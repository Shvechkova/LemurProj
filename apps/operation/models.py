from django.db import models
from django.utils import timezone
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum

from apps.service.models import ServicesMonthlyBill, SubcontractMonth


class MetaCategoryOperation(models.Model):
    name = models.CharField(max_length=200)
    
class SubCategoryOperation(models.Model):
    name = models.CharField(max_length=200)
    name2 = models.CharField(max_length=200, default="none")
    meta_categ = models.ForeignKey(
        MetaCategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Доп Категория операции",
        blank=True,
        null=True,
    )   
    
    META_CATEGORY = [
        ("oper_account", "oper_account"),
        ("banking", "banking"),
        ("nalog", "nalog"),
        ("salary", "salary"),
        ("suborders", "suborders"),
        ("entrering", "entrering"),
        ("none", "none"),
    ]
    meta_category = models.CharField(
        max_length=20, choices=META_CATEGORY, default="none"
    ) 
  

class CategoryOperation(models.Model):
    name = models.CharField(max_length=200)
    
    META_CATEGORY = [
        ("oper_account", "oper_account"),
        ("banking", "banking"),
        ("nalog", "nalog"),
        ("salary", "salary"),
        ("suborders", "suborders"),
        ("entrering", "entrering"),
        ("none", "none"),
    ]
    meta_categ = models.CharField(
        max_length=20, choices=META_CATEGORY, default="none"
    )
   

    # # SUB_CATEGORY = [
    # #     ("office", "Офис"),
    # #     ("marketing", "Реклама"),
    # #     ("other", "Прочее"),
    # #     ("0", "0"),
    # # ]
    # # sub_categ = models.CharField(
    # #     max_length=20, choices=SUB_CATEGORY, default="none"
    # # )
    sub_categ = models.ForeignKey(
        SubCategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Доп Категория операции",
        blank=True,
        null=True,
    )
    # sub_categor = models.ForeignKey(
    #     SubcatCategoryOperation,
    #     on_delete=models.PROTECT,
    #     verbose_name="Доп Категория операции",
    #     blank=True,
    #     null=True,
    # )
    # функция вывода операций для оперсчета

    # def get_operation_categ(self):
    #     months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    #               "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    #     year_now = datetime.now().year
    #     month_now = datetime.now().month
        
    #     # operation = Operation.objects.filter(category=self.id).annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id","comment","created_timestamp").order_by('month')
    #     # операции дял актуального года
    #     # operation = Operation.objects.filter(category=self.id, created_timestamp__year=year_now,
    #     #                                      created_timestamp__month__lte=month_now).annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp").order_by('month')
    #     # # операции прошлые годы
    #     # operation_old = Operation.objects.filter(category=self.id, created_timestamp__year__lt=year_now,
    #     #                                      ).annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp").order_by('month')
    #     # все операции
    #     operation = Operation.objects.filter(category=self.id).annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id", "comment", "created_timestamp").order_by('month')
    #     #
    #     dataset = []
       
    #     for month in range(1, month_now+1):
    #         dataset.append({
    #             "month": month,
    #             "month_name": months[month - 1],
    #         })
            
        

    #     for x in range(len(dataset)):
    #         dataset[x]['total'] = 0
    #         dataset[x]['absolute_total'] = 0
    #         dataset[x]['category'] = self.id
    #         dataset[x]['id_operation'] = ""
    #         dataset[x]['comments'] = []
    #         dataset[x]['year_now'] = year_now

    #         for y in range(len(operation)):
    #             if dataset[x]['year_now'] == operation[y]['created_timestamp'].year:

    #                 if dataset[x]['month'] == operation[y]['month'].month:

    #                     if dataset[x]['category'] == operation[y]['category']:
    #                         dataset[x]['total'] = dataset[x]['total'] + \
    #                             operation[y]['amount']
    #                         dataset[x]['year'] = operation[y]['created_timestamp'].year
    #                         dataset[x]['id_operation'] = dataset[x]['id_operation'] + \
    #                             str(operation[y]['id']) + "-"

    #                         if operation[y]['comment']:
    #                             comment = {
    #                                 "data": operation[y]['created_timestamp'],
    #                                 "sum": operation[y]['amount'],
    #                                 "comment": operation[y]['comment'],
    #                                 #  "name":oper.suborder.name,
    #                             }
    #                             dataset[x]['comments'].append(comment)

    #     dataset_old = [] 
    #     for month_old in range(1, 13):
    #         dataset_old.append({
    #             "month": month,
    #             # "month_name": months[month],
    #         })
    #     dataset_old_year = [] 
    #     last_oper_year = 0
    #     for oper_year  in operation:
    #         last_oper_year == oper_year['created_timestamp'].year
    #         if last_oper_year != oper_year['created_timestamp'].year:{
    #         dataset_old_year.append({
    #             "year": oper_year['created_timestamp'].year,
               
    #         })    
    #         }
            
            
              
        
    #     # print(operation_old)  
    #     # for x in range(len(dataset_old)):        
            
    #     # operation_old_years = []
    #     # operation_actual_years = [
    #     #     {
    #     #         "year_now": year_now,
    #     #     }
    #     # ]
    #     # for x in range(1, 12):
    #     #     # dataset[x]['total'] = 0
    #     #     # dataset[x]['absolute_total'] = 0
    #     #     # dataset[x]['category'] = self.id
    #     #     # dataset[x]['id_operation'] = ""
    #     #     # dataset[x]['comments'] = []
    #     #     dataset[x]['year_now'] = []
    #     #     dataset[x]['year_olds'] = []
    #     #     dataset[x]['category'] = self.id

    #     #     for y in range(len(operation)):
    #     #         if operation[y]['created_timestamp'].year == year_now:
    #     #             if x == operation[y]['month'].month:

    #     #                 if dataset[x]['category'] == operation[y]['category']:
    #     #                     dataset[x]['total'] = dataset[x]['total']  + operation[y]['amount']
    #     #                     dataset[x]['year'] = operation[y]['created_timestamp'].year
    #     #                     dataset[x]['id_operation']  = dataset[x]['id_operation'] + str(operation[y]['id']) + "-"

    #     #                     if operation[y]['comment']:
    #     #                         comment = {
    #     #                             "data": operation[y]['created_timestamp'],
    #     #                             "sum":operation[y]['amount'],
    #     #                             "comment":operation[y]['comment'],
    #     #                             #  "name":oper.suborder.name,
    #     #                         }
    #     #                         dataset[x]['comments'].append(comment)

    #     # print(operation_actual_years)
    #     # # операции для прошлых лет
    #     # operation_old = Operation.objects.filter(category=self.id,created_timestamp__year=year_now,
    #     #                                      created_timestamp__month__lte=month_now).annotate(month=TruncMonth('created_timestamp')).values('month').values("category", "month", 'amount', "id","comment","created_timestamp").order_by('month')

    #     dataset.reverse()

    #     return dataset
    # def get_operation_categ2(self):
    #     year_now = datetime.now().year
    #     month_now = datetime.now().month

    #     operation = Operation.objects.filter(category=self.id, bank=2, created_timestamp__year=year_now,
    #                                          created_timestamp__month__lte=month_now).annotate(month=TruncMonth('created_timestamp')).values('month').annotate(total=Sum('amount', default=0)).values("category", "month", 'total').order_by('month')

    #     dataset = []

    #     for month in range(1, month_now+1):
    #         dataset.append({
    #             "month": month,
    #         })

    #     for x in range(len(dataset)):
    #         dataset[x]['total'] = 0
    #         dataset[x]['absolute_total'] = 0
    #         dataset[x]['category'] = self.id

    #         for y in range(len(operation)):

    #             if dataset[x]['month'] == operation[y]['month'].month:

    #                 if dataset[x]['category'] == operation[y]['category']:
    #                     dataset[x]['total'] = operation[y]['total']

    #     dataset.reverse()

    #     return dataset


class NameOperation(models.Model):
    name = models.CharField(max_length=200)


class BankOperation(models.Model):
    name = models.CharField(max_length=200)
    slugish = models.CharField(max_length=200, blank=True, null=True)


class Operation(models.Model):
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    data = models.DateField(verbose_name="Дата добавления вручную"
                            )

    amount = models.PositiveIntegerField(default="0")

    comment = models.TextField("Комментарий", blank=True, null=True)

    bank = models.ForeignKey(
        BankOperation, on_delete=models.PROTECT, verbose_name="банк конечный назначения операции", blank=True, null=True
    )

    # bank_first = models.ForeignKey(
    #     BankOperation, on_delete=models.PROTECT, related_name='bank_first',verbose_name="банк начальный отправки операции", blank=True, null=True
    # )

    suborder = models.ForeignKey(
        SubcontractMonth,
        on_delete=models.PROTECT,
        verbose_name="Субподряд для оплат",
        blank=True,
        null=True,
    )

    name = models.ForeignKey(
        NameOperation,
        on_delete=models.PROTECT,
        verbose_name="Название операции",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        CategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Категория операции",
        blank=True,
        null=True,
    )
    meta_category = models.ForeignKey(
        MetaCategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Главная категория операции",
        blank=True,
        null=True,
    )

    monthly_bill = models.ForeignKey(
        ServicesMonthlyBill, on_delete=models.PROTECT, verbose_name="месячный счет для приходов и оплат", blank=True, null=True
    )

    TYPE_OPERATION = [
        ("entry", "entry"),
        ("out", "out"),
    ]

    type_operation = models.CharField(
        max_length=5, choices=TYPE_OPERATION, default="out"
    )

    META_CATEGORY = [
        ("oper_account", "oper_account"),
        ("banking", "banking"),
        ("nalog", "nalog"),
        ("salary", "salary"),
        ("suborders", "suborders"),
        ("entrering", "entrering"),
        ("none", "none"),
    ]
    meta_categ = models.CharField(
        max_length=20, choices=META_CATEGORY, default="none"
    )


class OperAccounts(models.Model):
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    # Запланированные траты
    amount = models.PositiveIntegerField(
        "сумма оплаты по оперсчету", default="0")


class OperAccountsName(models.Model):
    name = models.CharField("название типа расхода по оперсчету",
                            max_length=200, blank=True, null=True)
    meta_category = models.ForeignKey(
        MetaCategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Главная категория операции",
        blank=True,
        null=True,
    )


class OperAccountsNameSubcategory(models.Model):
    name = models.CharField("название типа субкатегории расхода по оперсчету",
                            max_length=200, blank=True, null=True)

    oper_accounts_name = models.ForeignKey(
        OperAccountsName,
        on_delete=models.PROTECT,
        verbose_name="название типа расхода по оперсчету",
        blank=True,
        null=True,
    )
