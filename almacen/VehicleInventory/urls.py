from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', vehicles, name='vehicles'),
    path('detail/<int:vehicle_id>/',  vehicle,  name='vehicle'),
]

