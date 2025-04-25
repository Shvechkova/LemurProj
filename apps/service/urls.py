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


# router.register(r"v1/service", view_sets.ClientViewSet)


# <int:client_id>/<slug:slug>

# path("<int:client_id>/<slug:slug>", views.addContract, name="contract"),
