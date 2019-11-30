from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', profiles, name='profiles'),
    path('producto/add/', producto_add, name='producto_add'),
    path('producto/add/confirma/', producto_confirma_add, name='producto_confirma_add'),
    path('proveedor/add/', proveedor_add, name='proveedor_add'),
    path('bodega/add/', bodega_add, name='bodega_add'),
    path('economico/add/', economico_add, name='economico_add'),
]

