from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', movimientos, name='movimientos'),
    path('detalle/<int:llanta_id>/', movimiento ,  name='movimiento'),
]

