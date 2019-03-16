from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', movimientos, name='movimientos'),
    path('salidas/', salidas, name='salidas'),
    path('salida/', salida, name='salida'),
    path('salida/<int:vale_id>/', salida_add, name='salida_add'),
    path('salida/<int:vale_id>/impresion/', salida_impresion, name='salida_impresion'),
    path('salida/<int:vale_id>/movimiento/', salida_add_movimiento, name='salida_add_movimiento'),
    path('detalle/<int:movimiento_id>/', movimiento ,  name='movimiento'),
    path('actual/', actual, name='actual'),
]

