from django.urls import include, path

from . import views
from rest_framework import routers
from .api import view_sets

app_name = "service"

router = routers.DefaultRouter()
router.register(r"api/service_category", view_sets.ServiceView)
router.register(r"api/month_bill", view_sets.ServicesMonthlyBillView)
# router.register(r"create-contract", views.CreateContract)
# basename="service"
# router.register(r'bill/client_list/', views.BillViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("ADV", views.adv_index, name="adv"),
    path("<int:client_id>", views.service_one, name="service_one"),
    path("", include(router.urls)),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
# <int:client_id>/<slug:slug>
