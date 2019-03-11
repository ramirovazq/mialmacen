"""almacen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from VehicleInventory import views as views_vehicleinventory
from VehicleInventory import urls as vehicleinventory_urls
from llantas import urls as llantas_urls

router = routers.DefaultRouter()
router.register(r'vehicles', views_vehicleinventory.VehicleViewSet)

urlpatterns = [
	path('v1/portal/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^llantas/', include(llantas_urls)),
    url(r'^vehicles/', include(vehicleinventory_urls)),
]
