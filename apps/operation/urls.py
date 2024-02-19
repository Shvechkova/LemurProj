from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views
from .api import view_sets
from rest_framework import routers


app_name = "operation"

router = routers.DefaultRouter()
router.register(r"api/entry", view_sets.OperationEntryViews)
router.register(r"api/out", view_sets.OperationOutViews)
router.register(r"api/operation", view_sets.OperationViews)



urlpatterns = [
    # path("", views.clients, name="client"),
    path("", include(router.urls)),
    # path("api/v1/clientlist/", ClientIpiView.as_view()),
    # path("", views.ClientView.as_view(), name="index"),
    # path("<int:client_id>", views.client, name="client"),
    # path("<int:client_id>/<slug:slug>", views.addContract, name="contract"),
    # path("<int:client_id>/<slug:slug>/sub", views.AddSubcontractors, name="sub"),
    # path("<int:client_id>/<slug:slug>/employee", views.add_employee, name="employee"),
    # path("<int:client_id>/<slug:slug>/adv", views.add_adv, name="adv"),
]
