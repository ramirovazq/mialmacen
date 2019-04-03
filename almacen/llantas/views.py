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
from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm, MovimientoSalidaForm, EntradaForm, NewLlantaForm, ImportacioMovimientosForm, AdjuntoValeForm
from .render_to_XLS_util import render_to_xls, render_to_csv
    

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
def entrada(request, tipo_movimiento="ENTRADA"):
    context = {}

    hoy = d_utils_now()
    fecha_hoy = hoy.strftime("%d-%m-%Y")    
    tm = TipoMovimiento.objects.get(nombre=tipo_movimiento)    
    profile_asociado = return_profile(request.user.username)
    initial_data = {'tipo_movimiento': tm, 'fecha_vale': fecha_hoy, 'creador_vale': profile_asociado}

    if request.method == 'POST':
        vale_instance = Vale(tipo_movimiento=tm, creador_vale=profile_asociado)
        form = EntradaForm(request.POST, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            return HttpResponseRedirect(reverse('entrada_add', args=[vale.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Error en formulario')
    else:
        form = EntradaForm(initial=initial_data)

    context["action"] = 'add'    
    context["form"] = form
    return render(request, 'entrada.html', context)

@login_required
def entrada_edit(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)

    if request.method == 'POST':
        #vale_instance = Vale(tipo_movimiento=tm, creador_vale=profile_asociado)
        form = EntradaForm(request.POST, instance=obj)#, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se guardan los cambios')
            return HttpResponseRedirect(reverse('entrada_add', args=[vale.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Error en formulario')

    else:
        form = EntradaForm(instance=obj)
    
    context["vale"] = obj
    context["form"] = form
    context["action"] = 'edit'
    return render(request, 'entrada.html', context)


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
def entrada_add(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)
    context['vale'] = obj

    if request.method == 'POST':
        form = NewLlantaForm(request.POST)

        if form.is_valid():
            existia, movimiento = form.save(obj)
            if existia:
                messages.add_message(request, messages.INFO, 'Ya existia una llanta con esas caracteristicas.')
            else:
                messages.add_message(request, messages.SUCCESS, 'Se crea una llanta con las nuevas caracteristicas.')
            messages.add_message(request, messages.SUCCESS, 'Se adiciona el movimiento de entrada {}'.format(movimiento))
            return HttpResponseRedirect(reverse('entrada_add', args=[obj.id]))    
    else:
        form = NewLlantaForm()

    context["adjuntosarchivos"] = AdjuntoVale.objects.filter(vale=obj).order_by('-fecha_created')
    context["form"] = form
    context["MEDIA_URL"] = settings.MEDIA_URL
    return render(request, 'entrada_add.html', context)


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
    return render(request, 'vales.html', context)    




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
def entrada_erase_movimiento(request, vale_id, movimiento_id):
    
    obj_vale = get_object_or_404(Vale, pk=vale_id)
    obj_movimiento = get_object_or_404(Movimiento, pk=movimiento_id)
    obj_movimiento.delete()

    messages.add_message(request, messages.SUCCESS, 'Se borra movimiento')
    return HttpResponseRedirect(reverse('entrada_add', args=[obj_vale.id]))


@login_required
def salida_impresion(request, vale_id):
    context = {}
    obj = get_object_or_404(Vale, pk=vale_id)
    context['vale'] = obj
    return render(request, 'formato.html', context)


@login_required
def entradas(request):
    context = {}
    v = Vale.objects.filter(tipo_movimiento__nombre='ENTRADA').order_by('-fecha_vale')
    
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    context["action"] = "entrada"
    return render(request, 'vales.html', context)    


@login_required
def importacion(request, tipo_movimiento="ENTRADA"):
    context = {}


    if request.method == 'POST':

        form = ImportacioMovimientosForm(request.POST, request.FILES)
        if form.is_valid():
            vale = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se subió con éxito el archivo')
            return HttpResponseRedirect(reverse('importacion'))
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, 'Error en formulario')
    else:
        form = ImportacioMovimientosForm()

    context["importacionarchivos"] = ImportacionMovimientos.objects.all().order_by('-fecha_created')
    context["action"] = 'import'    
    context["form"] = form
    return render(request, 'importacion.html', context)



@login_required
def entrada_adjuntar(request, vale_id):
    context = {}

    obj_vale = get_object_or_404(Vale, pk=vale_id)
    av = AdjuntoVale(vale=obj_vale)

    if request.method == 'POST':

        form = AdjuntoValeForm(request.POST, request.FILES)
        if form.is_valid():
            vale = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se subió con éxito el archivo')
            return HttpResponseRedirect(reverse('entrada_add', args=[obj_vale.id])) #, args=[vale.id]
        else:
            messages.add_message(request, messages.ERROR, 'Error en formulario')
    else:

        form = AdjuntoValeForm(instance=av)

    context["adjuntosarchivos"] = AdjuntoVale.objects.filter(vale=obj_vale).order_by('-fecha_created')
    context["form"] = form
    context["vale"] = obj_vale
    return render(request, 'adjuntar.html', context)
