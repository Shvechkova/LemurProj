from django.urls import path
from django.views.generic.base import TemplateView

from . import views


app_name = 'client'

urlpatterns = [
    path("", views.index, name="index"),
    # path("client/<int:client_number>", TemplateView.as_view(template_name="form_add_service.html")),
   
    path("clients/", views.ClientsListView.as_view(template_name="client/client_list.html"), name='clients'),
    # path("clients/<int:client>/", views.ClientViews.as_view(), name='client_one'),
    
]

#   path(
#         "karathons/<int:karathon_number>-karathon/",
#         views.KarathonView.as_view(),
#         name="karathon",
#     ),