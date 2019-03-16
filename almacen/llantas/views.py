from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now as d_utils_now

from rest_framework import viewsets
from datetime import datetime

from .utils import *
from .models import *
from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm
from .render_to_XLS_util import render_to_xls, render_to_csv

def post_filter(request, movimientos):

    tipo_movimiento = request.POST.get('tipo_movimiento', False)

    fecha_movimiento_inicio = request.POST.get('fecha_movimiento_inicio', '')
    fecha_movimiento_fin = request.POST.get('fecha_movimiento_fin', '')


    no_folio = request.POST.get('no_folio', False)

    marca = request.POST.get('marca', False)
    medida = request.POST.get('medida', False)
    posicion = request.POST.get('posicion', False)
    status = request.POST.get('status', '')

    dot = request.POST.get('dot', False)
    creador = request.POST.get('creador', False)


    fecha_creacion_inicio = request.POST.get('date_created_inicio', '')
    fecha_creacion_fin = request.POST.get('date_created_fin', '')

    origen = request.POST.get('origen', False)
    destino = request.POST.get('destino', False)


    ### new ... INICIO
    if tipo_movimiento:
      movimientos = movimientos.filter(vale__tipo_movimiento=tipo_movimiento)

    if fecha_movimiento_inicio:
        movimientos = movimientos.filter(fecha_movimiento__gte=datetime.strptime(fecha_movimiento_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if fecha_movimiento_fin:
        movimientos = movimientos.filter(fecha_movimiento__lte=datetime.strptime(fecha_movimiento_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))

    if fecha_creacion_inicio:
        print("uno")
        movimientos = movimientos.filter(date_created__gte=datetime.strptime(fecha_creacion_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if fecha_creacion_fin:
        print("dos ....")
        movimientos = movimientos.filter(date_created__lte=datetime.strptime(fecha_creacion_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))
    if no_folio:
        movimientos = movimientos.filter(vale__no_folio__icontains=no_folio)

    if origen:
        movimientos = movimientos.filter(origen__id=origen)
    if destino:
        movimientos = movimientos.filter(destino__id=destino)
    if marca:
        movimientos = movimientos.filter(marca__id=marca)
    if medida:
        movimientos = movimientos.filter(medida__id=medida)
    if posicion:
        movimientos = movimientos.filter(posicion__id=posicion)
    if status:
        movimientos = movimientos.filter(status__id=status)

    if dot:
        movimientos = movimientos.filter(dot__icontains=dot)
    if creador:
        movimientos = movimientos.filter(creador__id=creador)


    ### new ...FIN
    '''

    if producto:
      movimientos = movimientos.filter(producto__icontains=producto)

    if compania:
      movimientos = movimientos.filter(compania__icontains=compania)

    if propietario:
      movimientos = movimientos.filter(propietario__icontains=propietario)

    if detalle:
      movimientos = movimientos.filter(detalle__icontains=detalle)



    if ultima_actualizacion_inicio:
      movimientos = movimientos.filter(ultima_actualizacion__gte=datetime.strptime(ultima_actualizacion_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if ultima_actualizacion_fin:
      movimientos = movimientos.filter(ultima_actualizacion__lte=datetime.strptime(ultima_actualizacion_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))

    if fecha_programada_inicio:
      movimientos = movimientos.filter(fecha_programada__gte=datetime.strptime(fecha_programada_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if fecha_programada_fin:
      movimientos = movimientos.filter(fecha_programada__lte=datetime.strptime(fecha_programada_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))
    '''
    return movimientos

@login_required
def movimientos(request):
    context = {}
    m = Movimiento.objects.all().order_by('-fecha_movimiento')
    
    if request.method == 'POST':
        form = FilterMovimientoForm(request.POST)
        if form.is_valid():
            m = post_filter(request, m)            
    else:
        form = FilterMovimientoForm()
    
    context["form"] = form
    context["movimientos_count"] = m.count()

    ### export INI
    exporta = request.POST.get('exporta', False)
    exporta_xls = request.POST.get('exporta_xls', False)

    if exporta_xls == 'on':
        return render_to_xls(
            queryset=m,
            filename="export.xls"
        )                
    if exporta == 'on':
        return render_to_csv(
            queryset=m,
            filename="export.csv")
    ### export FIN

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


@login_required
def salida(request, tipo_movimiento="SALIDA"):
    context = {}

    hoy = d_utils_now()
    fecha_hoy = hoy.strftime("%d-%m-%Y")    
    tm = TipoMovimiento.objects.get(nombre=tipo_movimiento)    
    profile_asociado = return_profile(request.user.username)
    initial_data = {'tipo_movimiento': tm.id, 'fecha_vale': fecha_hoy, 'creador_vale': profile_asociado.id}

    if request.method == 'POST':
        vale_instance = Vale(tipo_movimiento=tm, creador_vale=profile_asociado)
        form = ValeForm(request.POST)#, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            return HttpResponseRedirect(reverse('salida_add', args=[vale.id]))
    else:
        form = ValeForm(initial=initial_data)
    
    context["form"] = form
    return render(request, 'salida.html', context)


@login_required
def salida_add(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)
    context['vale'] = obj

    search = Movimiento.objects.none()
    if request.method == 'POST':
        form = SearchSalidaForm(request.POST)

        if form.is_valid():
            search_filtrado = []
            dot = form.cleaned_data['dot']
            dicc_search, search, sin_entrada = Movimiento.actual_inventory("dot")

            for element in search:
                if dot in element[0]:
                    search_filtrado.append((element[0], element[1]))

            search = split_list(search_filtrado)
            search = sorted(search, key=lambda x: x[0][0]) 
            #Movimiento.actual_inventory('marca', form)
    else:
        form = SearchSalidaForm()


    columns_llanta_name = ["dot", "marca", "medida", "posicion"]
    context["columnas"] = columns_llanta_name
    context["form"] = form
    context['movimientos'] = search 
    return render(request, 'salida_add.html', context)

@login_required
def actual(request):
    context = {}

    orden = request.GET.get("orden", None)#default marca
    dicc_movimientos, lista_movimientos, sin_entrada = Movimiento.actual_inventory(orden)

    lista_movimientos = split_list(lista_movimientos)
    lista_movimientos = sorted(lista_movimientos, key=lambda x: x[0][0]) 
    #print("---------------")
    #print(lista_movimientos)


    if orden == 'marca':
        columns_llanta_name = ["Marca", "medida", "posicion", "dot"]
    elif orden == 'medida':
        columns_llanta_name = ["medida", "posicion", "dot", "marca"]
    elif orden == 'posicion':
        columns_llanta_name = ["posicion", "dot", "marca", "medida"]
    elif orden == 'dot':
        columns_llanta_name = ["dot", "marca", "medida", "posicion"]
    else:
        columns_llanta_name = ["Marca", "medida", "posicion", "dot"]
        lista_movimientos = sorted(lista_movimientos, key=lambda x: x[1]) 
        lista_movimientos.reverse()

    columns_llanta_name.append("Cantidad")
    context["columnas"] = columns_llanta_name

    context["movimientos"] = lista_movimientos
    return render(request, 'actual.html', context)    
