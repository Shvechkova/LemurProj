from django.db import models
from django.utils import timezone
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum

from apps.employee.models import Employee
from apps.service.models import ServicesMonthlyBill, SubcontractMonth


class BankOperation(models.Model):
    name = models.CharField(max_length=200)
    slugish = models.CharField(max_length=200, blank=True, null=True)


class MetaCategoryOperation(models.Model):
    name = models.CharField(max_length=200)


# добавить вручную для оперсчет офис реклама прочее банк
# добавить вручную для зап категории по типам


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
    bank = models.ForeignKey(
        BankOperation,
        on_delete=models.PROTECT,
        verbose_name="банк конечный назначения операции",
        blank=True,
        null=True,
    )


# добавить вручную для зп подкатегории


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
    meta_categ = models.CharField(max_length=20, choices=META_CATEGORY, default="none")

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


class NameOperation(models.Model):
    name = models.CharField(max_length=200)


class Operation(models.Model):
    created_timestamp = models.DateTimeField(
        default=timezone.now, verbose_name="Дата добавления"
    )
    data = models.DateField(verbose_name="Дата добавления вручную")
    amount = models.PositiveIntegerField(default="0")
    comment = models.TextField("Комментарий", blank=True, null=True)
    bank = models.ForeignKey(
        BankOperation,
        on_delete=models.PROTECT,
        verbose_name="банк конечный назначения операции",
        blank=True,
        null=True,
    )
    # bank_first = models.ForeignKey(
    #     BankOperation,
    #     on_delete=models.PROTECT,
    #     related_name="bank_first",
    #     verbose_name="банк начальный отправки операции",
    #     blank=True,
    #     null=True,
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
        ServicesMonthlyBill,
        on_delete=models.PROTECT,
        verbose_name="месячный счет для приходов и оплат",
        blank=True,
        null=True,
    )
    people = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name="зарплата",
        blank=True,
        null=True,
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
    meta_categ = models.CharField(max_length=20, choices=META_CATEGORY, default="none")


class OperAccounts(models.Model):
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )
    # Запланированные траты
    amount = models.PositiveIntegerField("сумма оплаты по оперсчету", default="0")


class OperAccountsName(models.Model):
    name = models.CharField(
        "название типа расхода по оперсчету", max_length=200, blank=True, null=True
    )
    meta_category = models.ForeignKey(
        MetaCategoryOperation,
        on_delete=models.PROTECT,
        verbose_name="Главная категория операции",
        blank=True,
        null=True,
    )


class OperAccountsNameSubcategory(models.Model):
    name = models.CharField(
        "название типа субкатегории расхода по оперсчету",
        max_length=200,
        blank=True,
        null=True,
    )

    oper_accounts_name = models.ForeignKey(
        OperAccountsName,
        on_delete=models.PROTECT,
        verbose_name="название типа расхода по оперсчету",
        blank=True,
        null=True,
    )
