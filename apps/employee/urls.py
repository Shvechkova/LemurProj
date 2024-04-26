from django.urls import include, path
from rest_framework import routers
from .api import view_sets

from . import views

app_name = 'employee'
router = routers.DefaultRouter()

router.register(r"api/employees", view_sets.EmployeeViews)

urlpatterns = [
    path("", views.employee, name="employee"),
    path("", include(router.urls)),
    # path("<int:worker_id>/", views.worker, name="workers"),
]