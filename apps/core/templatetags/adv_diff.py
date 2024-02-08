from django import template
from apps.service.models import Service, SubcontractMonth
from django.db.models import Count, Sum


register = template.Library()


@register.simple_tag()
def diff_adv_sum(all_sum=None,all_adv=None,):
    diff_adv = all_sum - all_adv
    return diff_adv

@register.simple_tag()
def sum_other(id_contract=None):
 
    subcontact_other_month = SubcontractMonth.objects.filter(id=id_contract)
    # .annotate(total_amount_other=Sum('amount'))
    
    return subcontact_other_month.
    


   