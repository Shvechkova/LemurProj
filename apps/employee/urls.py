from django.urls import path

from . import views

app_name = 'employee'

urlpatterns = [
    path("", views.employee, name="employee"),
    path("<int:worker_id>/", views.worker, name="workers"),
]