from django.utils import timezone
from django.db import models

from apps.operation.models import OperationEntry, OperationOut

# Create your models here.

# #отключить
# class BankAll(models.Model):
#     NAME = (
#         ("OOO", "ООО"),
#         ("IP", "ИП"),
#         ("$", "$"),
#         ("NONE", "---"),
#     )
#     # bank_name = models.CharField(max_length=200)

#     name = models.CharField(max_length=4, choices=NAME, default="NONE")

#     operation_entry = models.ForeignKey(
#         OperationEntry, on_delete=models.CASCADE, blank=True, null=True
#     )
#     operation_out = models.ForeignKey(
#         OperationOut, on_delete=models.CASCADE, blank=True, null=True
#     )
#     created_timestamp = models.DateTimeField(default=timezone.now)
#     # created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
