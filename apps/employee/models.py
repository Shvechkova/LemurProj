from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    TYPE = (
        ("INTERNAL", "Внешний"),
        ("EXTERNAL", "Внутренний"),
        
    )
    type = models.CharField(max_length=8, choices=TYPE, default="EXTERNAL")
    