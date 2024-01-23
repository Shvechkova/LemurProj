from django.urls import path
from django.views.generic.base import TemplateView

from . import views


app_name = 'client'

urlpatterns = [
    path("", views.clients, name="index" ),
    path("client/<int:client_id>", views.client, name="client" ),
    path("client/<int:client_id>/<slug:slug>", views.addContract, name="contract" ),
    path("client/<int:client_id>/<slug:slug>/sub", views.AddSubcontractors, name="sub" ),
    path("client/<int:client_id>/<slug:slug>/employee", views.add_employee, name="employee" ),
    path("client/<int:client_id>/<slug:slug>/adv", views.add_adv, name="adv" ),

    
]

