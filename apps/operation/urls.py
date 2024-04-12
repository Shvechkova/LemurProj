from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views
from .api import view_sets
from rest_framework import routers


app_name = "operation"

router = routers.DefaultRouter()
# router.register(r"api/entry", view_sets.OperationEntryViews)
# router.register(r"api/out", view_sets.OperationOutViews)
router.register(r"api/operation", view_sets.OperationViews)
router.register(r"api/add-category-office", view_sets.CategoryOperationViews)


urlpatterns = [

    path("", include(router.urls)),
    path("", views.index, name="index"),
    path("operation_inside", views.operation_inside, name="operation_inside"),
    path("oper_account", views.operation_inside_oper_account, name="oper_accaunt"),
    path("nalog", views.operation_inside_nalog, name="nalog"),
    path("bank_operation", views.operation_inside_bank, name="bank_operation"),
    path("salary", views.operation_inside_salary, name="salary"),
    
    path("operation_outside", views.operation_outside, name="operation_outside"),
    path("operation_storage", views.operation_storage, name="operation_storage"),

#     path("operation_outside/<slug:slug>", (views.operation_outside_categ),
#          name="operation_outside_categ"),
#     path("operation_inside/<slug:slug>", (views.operation_inside_categ),
#          name="operation_inside_categ"),


    # path("api/v1/clientlist/", ClientIpiView.as_view()),
    # path("", views.ClientView.as_view(), name="index"),
    # path("<int:client_id>", views.client, name="client"),
    # path("<int:client_id>/<slug:slug>", views.addContract, name="contract"),
    # path("<int:client_id>/<slug:slug>/sub", views.AddSubcontractors, name="sub"),
    # path("<int:client_id>/<slug:slug>/employee", views.add_employee, name="employee"),
    # path("<int:client_id>/<slug:slug>/adv", views.add_adv, name="adv"),
]
