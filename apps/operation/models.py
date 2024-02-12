from django.db import models

from apps.service.models import ServicesMonthlyBill


class CategoryOperation(models.Model):
    name = models.CharField(max_length=200)
    
class MetaCategoryOperation(models.Model):
    name = models.CharField(max_length=200)    


class NameOperation(models.Model):
    name = models.CharField(max_length=200)
    
class BankOperation(models.Model):
    name = models.CharField(max_length=200)


class OperationEntry(models.Model):
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    amount = models.PositiveIntegerField(default="0")

    comment = models.TextField("Комментарий", blank=True, null=True)

    name = models.ForeignKey(
        NameOperation, on_delete=models.PROTECT, blank=True, null=True
    )
    bank = models.ForeignKey(
        BankOperation, on_delete=models.PROTECT, blank=True, null=True
    )
    category = models.ForeignKey(
        CategoryOperation, on_delete=models.PROTECT, blank=True, null=True
    )
    # comment = models.TextField("Комментарий", blank=True, null=True)
    
    monthly_bill = models.ForeignKey(
        ServicesMonthlyBill, on_delete=models.PROTECT, blank=True, null=True
    )





class OperationOut(models.Model):
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    sum = models.PositiveIntegerField(default="0")
    comment = models.TextField("Комментарий", blank=True, null=True)
    BANK = (
        ("OOO", "ООО"),
        ("IP", "ИП"),
        ("$", "$"),
    )

    bank = models.CharField(max_length=4, choices=BANK, verbose_name="Счет поступления",  default="OOO")
    name = models.ForeignKey(
        NameOperation, on_delete=models.PROTECT, verbose_name="Название операции", blank=True, null=True
    )
    category = models.ForeignKey(
        CategoryOperation, on_delete=models.PROTECT,verbose_name="Категория операции",  blank=True, null=True
    )
    meta_category = models.ForeignKey(
        MetaCategoryOperation, on_delete=models.PROTECT,verbose_name="Главная категория операции",  blank=True, null=True
    )
    comment = models.TextField("Комментарий", blank=True, null=True)
