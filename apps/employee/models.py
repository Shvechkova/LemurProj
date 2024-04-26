from django.db import models


# Create your models here.
class CategoryEmployee(models.Model):
    name = models.CharField(max_length=200)


class Employee(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    TYPE = (
        ("INTERNAL", "Внешний"),
        ("EXTERNAL", "Внутренний"),
    )
    type = models.CharField(max_length=8, choices=TYPE, default="EXTERNAL")
    category = models.ForeignKey(
        CategoryEmployee,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
    )
    date_start = models.DateField("Дата начала действия", blank=True, null=True)
    date_end = models.DateField("Дата окончания", blank=True, null=True)
    
