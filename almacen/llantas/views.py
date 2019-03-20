from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now as d_utils_now

from rest_framework import viewsets
from datetime import datetime

from .utils import *
from .models import *
from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm, MovimientoSalidaForm
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
def salida_edit(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)

    if request.method == 'POST':
        #vale_instance = Vale(tipo_movimiento=tm, creador_vale=profile_asociado)
        form = ValeForm(request.POST, instance=obj)#, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se guardan los cambios')
            return HttpResponseRedirect(reverse('salida_add', args=[vale.id]))
    else:
        form = ValeForm(instance=obj)
    
    context["vale"] = obj
    context["form"] = form
    context["action"] = 'edit'
    return render(request, 'salida.html', context)


@login_required
def salida_add(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)
    context['vale'] = obj

    search = Llanta.objects.none()
    if request.method == 'POST':
        form = SearchSalidaForm(request.POST)

        if form.is_valid():
            search_filtrado = []
            dot = form.cleaned_data['dot']
            search = Llanta.objects.filter(dot__icontains=dot)
    else:
        form = SearchSalidaForm()

    context["form"] = form
    context['form_salida'] = MovimientoSalidaForm()
    context['llantas'] = search 
    return render(request, 'salida_add.html', context)

@login_required
def actual(request):
    context = {}

    llantas = Llanta.objects.all()
    numero_llantas = sum([x.cantidad_actual_total() for x in llantas])
    context['numero_llantas'] = numero_llantas

    orden = request.GET.get("orden", None)#default marca

    if orden == 'marca':
        llantas = llantas.order_by('marca__nombre')
    elif orden == 'medida':
        llantas = llantas.order_by('medida__nombre')
    elif orden == 'posicion':
        llantas = llantas.order_by('posicion__nombre')
    elif orden == 'dot':
        llantas = llantas.order_by('dot')
    elif orden == 'status':
        llantas = llantas.order_by('status__nombre')
    elif orden == 'cantidad':
        l = []
        for llanta in llantas:
            l.append((llanta, llanta.cantidad_actual_total()))
        l = sorted(l, key=lambda x: x[1])
        l.reverse()
        llantas = l    
    else:
        llantas = llantas.order_by('marca__nombre')

    context['orden'] = orden        
    context['llantas'] = llantas
    return render(request, 'actual.html', context)    


@login_required
def salidas(request):
    context = {}
    v = Vale.objects.filter(tipo_movimiento__nombre='SALIDA').order_by('-fecha_vale')
    
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    return render(request, 'vales_salida.html', context)    




@login_required
def salida_add_movimiento(request, vale_id):
    
    obj = get_object_or_404(Vale, pk=vale_id)

    if request.method == 'POST':
        form = MovimientoSalidaForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad'] 
            id_llanta = request.POST['id_llanta']
            llanta  = get_object_or_404(Llanta, pk=id_llanta)
            nombre_origen = request.POST['nombre_origen']
            #llanta  = Llanta.objects.get(id=id_llanta)
            origen  = return_profile(nombre_origen, "BODEGA")
            creador  = return_profile(request.user.username, "STAFF")

            dicc_ubicaciones = llanta.total_ubicaciones()
            cantidad_en_ubicacion = dicc_ubicaciones[origen.user.username]
            if cantidad <= cantidad_en_ubicacion: ## extra validacion, solo puede sacarse una cantidad menor o igual a lo existente
                m = Movimiento(
                    vale=obj, 
                    tipo_movimiento=obj.tipo_movimiento,
                    fecha_movimiento=obj.fecha_vale,                
                    origen=origen,
                    destino=form.cleaned_data['destino'],
                    llanta=llanta,
                    cantidad=form.cleaned_data['cantidad'],
                    observacion=form.cleaned_data['observacion'],
                    creador=creador
                )
                m.save()
                messages.add_message(request, messages.SUCCESS, 'Se adiciona movimiento {}'.format(m.id))
                return HttpResponseRedirect(reverse('salida_add', args=[obj.id]))    
            else:
                messages.add_message(request, messages.ERROR, 'No se puede sacar una cantidad mayor a la que existente en la ubicacion')        
                return HttpResponseRedirect(reverse('salida_add', args=[obj.id]))


    messages.add_message(request, messages.ERROR, 'Error en formulario')        
    return HttpResponseRedirect(reverse('salida_add', args=[obj.id]))

@login_required
def salida_erase_movimiento(request, vale_id, movimiento_id):
    
    obj_vale = get_object_or_404(Vale, pk=vale_id)
    obj_movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    obj_movimiento.delete()

    messages.add_message(request, messages.SUCCESS, 'Se borra movimiento')
    return HttpResponseRedirect(reverse('salida_add', args=[obj_vale.id]))


@login_required
def salida_impresion(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)
    context['vale'] = obj
    return render(request, 'formato.html', context)
