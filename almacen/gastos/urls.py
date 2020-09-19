from django.conf.urls import url
from django.urls import path

from .views import registro, registros

urlpatterns = [
    path('', registros, name='registros'),    
    path('registro/', registro, name='registro'),
]

