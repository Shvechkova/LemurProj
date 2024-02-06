from django import template
from apps.service.models import Service


register = template.Library()

@register.simple_tag()
def categorys():
    return Service.objects.all()

# @register.inclusion_tag("service/includes/service_menu.html", takes_context=True)
# def category_service(context):
#     service_list = Service.objects.all()
    

#     return {
#         "service_list": service_list,
#         # "view_name": context.request.resolver_match.view_name,
        
#     }
    
    