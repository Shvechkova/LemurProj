from django.urls import path
from django.views.generic.base import TemplateView

from . import views


app_name = 'client'

urlpatterns = [
    path("", views.clients, name="index" ),
    path("client/<int:client_id>", views.client, name="client" ),
    
]

