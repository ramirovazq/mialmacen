from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

from rest_framework import viewsets

from .models import *

@login_required
def movimientos(request):
    context = {}
    m = Movimiento.objects.all().order_by('-fecha_movimiento')
    

    paginator = Paginator(m, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    m = paginator.get_page(page)

    context["movimientos"] = m
    return render(request, 'movimientos.html', context)    

@login_required
def movimiento(request, movimiento_id):
    context = {}
    movimiento = get_object_or_404(Movimiento, id=movimiento_id)
    context["movimiento"] = movimiento
    return render(request, 'movimiento.html', context)    


#class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
 #   queryset = Vehicle.objects.all().order_by('-creation_date')
  #  serializer_class = VehicleSerializer