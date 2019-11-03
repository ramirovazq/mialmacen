from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', movimientos_general, name='movimientos_general'),

    #path('importacion/', importacion, name='importacion'),
    #path('entradas/', entradas, name='entradas'),
    #path('salidas/', salidas, name='salidas'),

    path('vales/', vales_general, name='vales_general'),
    path('vale/<int:vale_id>/erase/', vale_general_erase, name='vale_general_erase'),

    path('salida/', salida_general, name='salida_general'),
    path('entrada/', entrada_general, name='entrada_general'),

    #path('salida/<int:vale_id>/edit/', salida_edit, name='salida_edit'),
    #path('entrada/<int:vale_id>/edit/', entrada_edit, name='entrada_edit'),
    path('salida/<int:vale_id>/', salida_general_add, name='salida_general_add'),
    path('entrada/<int:vale_id>/', entrada_detail, name='entrada_detail'),
    #path('entrada/<int:vale_id>/adjuntar/', entrada_adjuntar, name='entrada_adjuntar'),
    path('salida/<int:vale_id>/impresion/', salida_general_impresion, name='salida_general_impresion'),
    path('salida/<int:vale_id>/movimiento/', salida_general_add_movimiento, name='salida_general_add_movimiento'),


    path('salida/<int:vale_id>/movimiento/<int:movimiento_id>/erase/', salida_general_erase_movimiento, name='salida_general_erase_movimiento'),
    #path('entrada/<int:vale_id>/movimiento/<int:movimiento_id>/erase/', entrada_erase_movimiento, name='entrada_erase_movimiento'),    
    #path('detalle/<int:movimiento_id>/', movimiento ,  name='movimiento'),
    
    path('actual/', actual_general, name='actual_general'),
    path('detalle/<int:producto_id>/movimientos/', producto_detalle, name='producto_detalle'),

]

