from django.urls import include, path

from . import views

app_name = 'service'

from rest_framework import routers


# urlpatterns = [
#     # path("", views.index, name="index"),
#     # path("<slug:slug>", views.serviced, name="serviced"),
#     path('', include((router.urls))),
# ]

# urlpatterns = [
#     path('', include(router.urls)),
#     # path('1/', include('rest_framework.urls', namespace='rest_framework'))
    
# ]
router = routers.DefaultRouter()
router.register(r'bill', views.BillViewSet )
router.register(r'create-contract', views.CreateContract)
# basename="service"
# router.register(r'bill/client_list/', views.BillViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.index, name="index"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]