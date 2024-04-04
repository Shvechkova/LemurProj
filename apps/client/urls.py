from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views
from .api import view_sets
from rest_framework import routers


app_name = "client"

router = routers.DefaultRouter()
router.register(r"api/client", view_sets.AddClient)
router.register(r"api/contract", view_sets.ContractView)
# router.register(r"api/additional_contract", view_sets.AdditionalContractView)


urlpatterns = [
    path("", views.clients, name="client"),
    path("", include(router.urls)),
    # path("api/v1/clientlist/", ClientIpiView.as_view()),
    # path("", views.ClientView.as_view(), name="index"),
    # path("<int:client_id>", views.client, name="client"),
    # path("<int:client_id>/<slug:slug>", views.addContract, name="contract"),
    # path("<int:client_id>/<slug:slug>/sub", views.AddSubcontractors, name="sub"),
    # path("<int:client_id>/<slug:slug>/employee", views.add_employee, name="employee"),
    # path("<int:client_id>/<slug:slug>/adv", views.add_adv, name="adv"),
]
