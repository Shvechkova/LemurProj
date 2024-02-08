from django import template
from apps.service.models import Service, SubcontractMonth
from django.db.models import Count, Sum


register = template.Library()


@register.simple_tag()
def diff_adv_sum(all_sum=None, all_adv=None,):
    diff_adv = all_sum - all_adv
    return diff_adv


@register.simple_tag()
def sum_other(id_contract=None):

    sub_sum = SubcontractMonth.objects.filter(
        month_bill=id_contract, other__isnull=False).aggregate(Sum("amount"))
    sum_actual = sub_sum.get("amount__sum")
   
    c = str(sum_actual) + "₽" 
    if sum_actual != None :
        return c
    else: return ''

    
