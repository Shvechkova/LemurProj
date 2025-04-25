from django.urls import include, path

from . import views
from rest_framework import routers
from .api import view_sets
from django.views.decorators.cache import cache_page

app_name = "service"

router = routers.DefaultRouter()
router.register(r"api/service_category", view_sets.ServiceView)
router.register(r"api/month_bill", view_sets.ServicesMonthlyBillView)
router.register(r"api/subcontract-category-adv", view_sets.SubcontractCategoryAdvView)
router.register(r"api/subcontract-category-other", view_sets.SubcontractCategoryOtherView)
router.register(r"api/subcontract", view_sets.SubcontractMonthView)
# router.register(r"create-contract", views.CreateContract)
# basename="service"
# router.register(r'bill/client_list/', views.BillViewSet)


urlpatterns = [
    path("", views.index, name="index"),
     path("new_month", views.new_month, name="new_month"),
    # path("ADV", views.adv_index, name="adv"),
    # path("<int:client_id>", views.service_one, name="service_one"),
    path("", include(router.urls)),
    path("<slug:slug>",(views.service_one),name="service_one"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
# <int:client_id>/<slug:slug>

# path("<int:client_id>/<slug:slug>", views.addContract, name="contract"),
