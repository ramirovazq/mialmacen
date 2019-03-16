from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', movimientos, name='movimientos'),
    path('salida/', salida, name='salida'),
    path('salida/<int:vale_id>/', salida_add, name='salida_add'),
    path('detalle/<int:movimiento_id>/', movimiento ,  name='movimiento'),
    path('actual/', actual, name='actual'),
]

