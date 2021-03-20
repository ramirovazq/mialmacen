from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.authtoken import views as views_rest_framwork
from VehicleInventory import views as views_vehicleinventory
from VehicleInventory import urls as vehicleinventory_urls
from gastos import urls as gastos_urls
from llantas import urls as llantas_urls
from general import urls as general_urls
from llantas import urls_api as llantas_api_urls
from persona import urls as profiles_urls
from login_recover import views as login_recover_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^api/v0/login/$', login_recover_views.Login.as_view(), name='api_login'),
	path('api/v0/', include(llantas_api_urls)),
	#path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),    
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^gastos/', include(gastos_urls)),
    url(r'^llantas/', include(llantas_urls)),
    url(r'^general/', include(general_urls)),    
    url(r'^profiles/', include(profiles_urls)),    
    url(r'^vehicles/', include(vehicleinventory_urls)),
    url(r'^apiref/', views.SwaggerSchemaView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
