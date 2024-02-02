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
    
