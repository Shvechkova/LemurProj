# from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

# router.registry.extend(client_router.registry)
# from . import views
urlpatterns = [
     path('__debug__/', include('debug_toolbar.urls')),
    path("admin/", admin.site.urls),
    
    path("", include("apps.core.urls", namespace="core")),
    path("service/", include("apps.service.urls", namespace="service")),
    path("clients/", include("apps.client.urls", namespace="clients")),
    path("employee/", include("apps.employee.urls", namespace="employees")),
    path("operations/", include("apps.operation.urls", namespace="operation")),
    path("bank/", include("apps.bank.urls", namespace="bank")),
    path('api/', include('rest_framework.urls')),
    path("apiV1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)