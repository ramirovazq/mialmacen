from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', home_llantas, name='home_llantas'),    
    path('movimientos/', movimientos, name='movimientos'),
    path('importacion/', importacion, name='importacion'),
    #path('entradas/', entradas, name='entradas'),
    #path('salidas/', salidas, name='salidas'),
    path('basura/', basura_vales, name='basura_vales'),
    path('vales/', vales, name='vales'),

    path('vale/<int:vale_id>/erase/', vale_erase, name='vale_erase'),
    path('vale/<int:vale_id>/basura/erase/', vale_erase_basura, name='vale_erase_basura'),

    path('salida/', salida, name='salida'),
    path('entrada/', entrada, name='entrada'),

    path('entrada/basura/', entrada_basura, name='entrada_basura'),

    path('salida/<int:vale_id>/edit/', salida_edit, name='salida_edit'),
    path('entrada/<int:vale_id>/edit/', entrada_edit, name='entrada_edit'),


    path('entrada/basura/<int:vale_id>/edit/', entrada_basura_edit, name='entrada_basura_edit'),

    path('salida/<int:vale_id>/', salida_add, name='salida_add'),
    path('entrada/<int:vale_id>/', entrada_add, name='entrada_add'),

    path('entrada/basura/<int:vale_id>/', entrada_basura_add, name='entrada_basura_add'),

    path('salida/<int:vale_id>/adjuntar/', salida_adjuntar, name='salida_adjuntar'),
    path('entrada/<int:vale_id>/adjuntar/', entrada_adjuntar, name='entrada_adjuntar'),
    path('salida/<int:vale_id>/impresion/', salida_impresion, name='salida_impresion'),
    path('salida/<int:vale_id>/movimiento/', salida_add_movimiento, name='salida_add_movimiento'),
    path('salida/<int:vale_id>/movimiento/<int:movimiento_id>/erase/', salida_erase_movimiento, name='salida_erase_movimiento'),
    path('entrada/<int:vale_id>/movimiento/<int:movimiento_id>/erase/', entrada_erase_movimiento, name='entrada_erase_movimiento'),    

    path('entrada/<int:vale_id>/movimiento/<int:movimiento_id>/basura/erase/', entrada_erase_movimiento_basura, name='entrada_erase_movimiento_basura'),    

    path('detalle/<int:movimiento_id>/', movimiento ,  name='movimiento'),
    path('actual/', actual, name='actual'),
    path('llanta/<int:llanta_id>/movimientos/', llanta_detalle, name='llanta_detalle'),
]

