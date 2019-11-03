from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now as d_utils_now

#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .models import *
from persona.models import Profile, Tipo, ProfilePosition
from .forms import FilterMovimientoForm
from llantas.utils import return_profile
from .forms import ValeAlmacenGeneralForm, SearchSalidaGeneralForm, MovimientoSalidaGeneralForm
#from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm, MovimientoSalidaForm, EntradaForm, NewLlantaForm, ImportacioMovimientosForm, AdjuntoValeForm, ProfileSearchForm
#from .render_to_XLS_util import render_to_xls, render_to_csv, render_to_xls_inventario
#from .serializers import ValeSerializer, LlantaSerializer, ProfileSerializer, MovimientoSerializer

@login_required
def movimientos_general(request):
    context = {}
    m = MovimientoGeneral.objects.all().order_by('-fecha_movimiento')
    
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
    return render(request, 'movimientos_general.html', context)    


@login_required
def vales(request):
    context = {}
    action = request.GET.get("tipo", "ENTRADA")
    
    if action:
        action = action.upper()

    v = ValeAlmacenGeneral.objects.filter(tipo_movimiento__nombre=action).order_by('-fecha_vale', '-no_folio')
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    context["action"] = action
    return render(request, 'vales_general.html', context)    


@login_required
def entrada_detail(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
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
    return render(request, 'entrada_general_detail.html', context)


@login_required
def actual_general(request):
    context = {}

    llantas = Producto.objects.all()

    orden = request.GET.get("orden", None)#default marca
    export = request.GET.get("export", None)#default marca

    full_path = request.get_full_path()
    if "?" in full_path:
        url_export = full_path + '&export=True'
    else:
        url_export = '?export=True'

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
        llantas = llantas.order_by('nombre')


    if export:
        return render_to_xls_inventario(
                queryset=llantas,
                filename="export_inventario.xls"
            )                

    context['orden'] = orden        
    context['productos'] = llantas
    context['url_export'] = url_export

    return render(request, 'actual_general.html', context)    


@login_required
def producto_detalle(request, producto_id):
    context = {}
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad, unidad_referencia = producto.inventory()

    context["producto"] = producto
    context["cantidad"] = cantidad
    context["unidad"] = unidad_referencia
    
    return render(request, 'producto.html', context)    


@login_required
def salida_general(request, tipo_movimiento="SALIDA"):
    context = {}

    hoy = d_utils_now()
    fecha_hoy = hoy.strftime("%d-%m-%Y")    
    tm = TipoMovimiento.objects.get(nombre=tipo_movimiento)    
    profile_asociado = return_profile(request.user.username)
    initial_data = {'tipo_movimiento': tm.id, 'fecha_vale': fecha_hoy, 'creador_vale': profile_asociado.id}

    if request.method == 'POST':
        vale_instance = ValeAlmacenGeneral(tipo_movimiento=tm, creador_vale=profile_asociado)
        form = ValeAlmacenGeneralForm(request.POST)#, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            return HttpResponseRedirect(reverse('salida_general_add', args=[vale.id]))
    else:
        form = ValeAlmacenGeneralForm(initial=initial_data)
    
    context["form"] = form
    return render(request, 'salida_general.html', context)

@login_required
def entrada_general(request, tipo_movimiento="ENTRADA"):
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
    return render(request, 'entrada_general.html', context)


@login_required
def salida_general_add(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    context['vale'] = obj

    search = Producto.objects.none()

    if request.method == 'POST':
            form = SearchSalidaGeneralForm(request.POST)
            if form.is_valid():
                search_filtrado = []

                dicc_llanta = {}
                prod = form.cleaned_data['nombre']
                if prod:
                    dicc_llanta['nombre'] = prod.nombre

                if dicc_llanta.keys():
                    messages.add_message(request, messages.INFO, 'Búsqueda por: {}'.format(dicc_llanta))
                    search = Producto.objects.filter(**dicc_llanta)
                else:
                    messages.add_message(request, messages.INFO, 'Selecciona almenos un criterio de búsqueda.')
    else:
        form = SearchSalidaGeneralForm()

    context['form_salida'] = MovimientoSalidaGeneralForm()
    context["form"] = form
    context['productos'] = search 
    return render(request, 'salida_general_add.html', context)


@login_required
def vale_general_erase(request, vale_id):
    redirige_entrada = None
    obj_vale = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    if len(obj_vale.movimientos()) == 0:
        obj_vale.delete()
        messages.add_message(request, messages.SUCCESS, 'Se borró el Vale de salida del almacen general')
    else:
        messages.add_message(request, messages.WARNING, 'Este vale tiene movimientos, no se puede borrar.')
    return HttpResponseRedirect(reverse('vales_general')+"?tipo="+obj_vale.tipo_movimiento.nombre)


@login_required
def salida_general_add_movimiento(request, vale_id):
    
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)

    if request.method == 'POST':
        form = MovimientoSalidaGeneralForm(request.POST)
        if form.is_valid():

            cantidad = form.cleaned_data['cantidad']
            cantidad_max = request.POST['cantidad_max']
            id_producto = request.POST['id_producto']
            id_origen = request.POST['id_origen']
            id_profileposition = request.POST['id_profileposition']
            producto  = get_object_or_404(Producto, pk=id_producto)
            origen = get_object_or_404(Profile, pk=id_origen)
            profileposition = get_object_or_404(ProfilePosition, pk=id_profileposition)

            creador  = return_profile(request.user.username, "STAFF")

            dicc_movimiento = {
                    "vale":obj, 
                    "tipo_movimiento":obj.tipo_movimiento,
                    "fecha_movimiento":obj.fecha_vale,                

                    "origen":origen,
                    "producto":producto,                    

                    "unidad": form.cleaned_data['unidad'],
                    "cantidad":form.cleaned_data['cantidad'],
                    "observacion":form.cleaned_data['observacion'],
                    "destino":form.cleaned_data['destino'],

                    "creador":creador
            }

            if float(cantidad) <= float(cantidad_max): ## extra validacion, solo puede sacarse una cantidad menor o igual a lo existente
                m = MovimientoGeneral(**dicc_movimiento)
                m.save()

                ProductoExactProfilePosition.objects.create(
                    exactposition=profileposition, #nivel_twenty_three
                    movimiento=m
                )

                messages.add_message(request, messages.SUCCESS, 'Se adiciona movimiento {}'.format(m.id))
                return HttpResponseRedirect(reverse('salida_general_add', args=[obj.id]))    
            else:
                messages.add_message(request, messages.ERROR, 'No se puede sacar una cantidad mayor a la que existente en la ubicacion')        
                return HttpResponseRedirect(reverse('salida_general_add', args=[obj.id]))


    messages.add_message(request, messages.ERROR, 'Error en formulario')        
    return HttpResponseRedirect(reverse('salida_general_add', args=[obj.id]))

@login_required
def salida_general_erase_movimiento(request, vale_id, movimiento_id):
    
    obj_vale = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    obj_movimiento = get_object_or_404(MovimientoGeneral, pk=movimiento_id)
    for productoexactprofileposition in obj_movimiento.le_positions():
        productoexactprofileposition.delete()
    obj_movimiento.delete()

    messages.add_message(request, messages.SUCCESS, 'Se borra movimiento')
    return HttpResponseRedirect(reverse('salida_general_add', args=[obj_vale.id]))

@login_required
def salida_general_impresion(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    context['vale'] = obj
    return render(request, 'formato_general.html', context)
