from django import template
from apps.service.models import Service


register = template.Library()


@register.simple_tag()
def diff_adv_sum(all_sum=None,all_adv=None,):
    diff_adv = all_sum - all_adv
    return diff_adv
   