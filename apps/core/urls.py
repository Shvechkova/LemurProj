
from django.urls import include, path



from . import views

# router.register(r'accounts', AccountViewSet)
app_name = 'core'

urlpatterns = [
    path("", views.index, name="home"),
    # path('api/', include((router.urls))),
    
]