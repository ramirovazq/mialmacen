from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now as d_utils_now
from django.db.models import Q

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
from llantas.utils import return_profile
from .forms import ValeAlmacenGeneralForm, SearchSalidaGeneralForm, MovimientoSalidaGeneralForm, FilterMovimientoForm
from .forms import MovimientoEntradaGeneralForm, EntradaGeneralForm, PositionForm
#from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm, MovimientoSalidaForm, EntradaForm, NewLlantaForm, ImportacioMovimientosForm, AdjuntoValeForm, ProfileSearchForm
#from .render_to_XLS_util import render_to_xls, render_to_csv, render_to_xls_inventario
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)

    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def search_product(self, request):
        productos_serializados = ProductoSerializer()
        if 'query' in request.query_params.keys():
            search = request.query_params.get('query')
            if len(search) >= 3:

                lista_productos = Producto.objects.filter(
                    nombre__icontains=search
                ).values('id')
                lista_productos = [x['id'] for x in lista_productos]

                lista_productos_np = NumeroParte.objects.filter(
                    numero_de_parte__icontains=search
                ).values('producto__id')
                lista_productos_np = [x['producto__id'] for x in lista_productos_np]

                lista_productos_suma = set(lista_productos+lista_productos_np)                
                productos = Producto.objects.filter(id__in=lista_productos_suma)
                
                productos_serializados = ProductoSerializer(productos, many=True)
        return Response(productos_serializados.data)

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
def vales_general(request):
    context = {}
    action = request.GET.get("tipo", "ENTRADA")
    
    if action:
        action = action.upper()

    v = ValeAlmacenGeneral.objects.filter(tipo_movimiento__nombre=action, vale_llantas=False).order_by('-fecha_vale', '-no_folio')
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    context["action"] = action
    return render(request, 'vales_general.html', context)    




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

    paginator = Paginator(llantas, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    llantas = paginator.get_page(page)


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
        vale_instance = ValeAlmacenGeneral(tipo_movimiento=tm, creador_vale=profile_asociado, vale_llantas=False)
        form = ValeAlmacenGeneralForm(request.POST, instance=vale_instance)
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
        vale_instance = ValeAlmacenGeneral(tipo_movimiento=tm, creador_vale=profile_asociado, vale_llantas=False)
        form = EntradaGeneralForm(request.POST, instance=vale_instance)
        if form.is_valid():
            vale = form.save()
            return HttpResponseRedirect(reverse('entrada_general_add', args=[vale.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Error en formulario')
    else:
        form = EntradaGeneralForm(initial=initial_data)

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
def entrada_general_add(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    context['vale'] = obj

    if request.method == 'POST':
        profile_asociado = return_profile(request.user.username)
        movimiento_instance = MovimientoGeneral(
                vale=obj,
                tipo_movimiento=obj.tipo_movimiento,
                fecha_movimiento=obj.fecha_vale,
                origen=obj.persona_asociada,
                creador=profile_asociado)
        form = MovimientoEntradaGeneralForm(request.POST, instance=movimiento_instance) # MovimientoGeneral
        if form.is_valid():
            mov = form.save()
            messages.add_message(request, messages.SUCCESS, 'Movimiento de entrada insertado: {}'.format(mov.id))
            return HttpResponseRedirect(reverse('entrada_general_add', args=[obj.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Revisa el formulario')
    else:
        form = MovimientoEntradaGeneralForm()

    context['form_position'] = PositionForm()
    context["form"] = form
    return render(request, 'entrada_general_add.html', context)

@login_required
def entrada_general_add_movimiento_position(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)

    if request.method == 'POST':
        id_movimiento = request.POST['id_movimiento']
        movimiento  = get_object_or_404(MovimientoGeneral, pk=id_movimiento)        
        position_instance = ProductoExactProfilePosition(
            movimiento=movimiento
        )
        form = PositionForm(request.POST, instance=position_instance) # MovimientoGeneral
        if form.is_valid():
            productexact = form.save()
            movimiento.destino = productexact.exactposition.profile
            movimiento.save()
            messages.add_message(request, messages.SUCCESS, 'Se asocia una posicion para el producto de forma exitosa')
        else:
            messages.add_message(request, messages.ERROR, 'No se pudo asociar un producto a una posicion')
    print("...............obj")
    print(obj)
    print(obj.id)
    return HttpResponseRedirect(reverse('entrada_general_add', kwargs={"vale_id": obj.id}))


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

            unidad = form.cleaned_data['unidad']
            cantidad = form.cleaned_data['cantidad']
            cantidad_en_unidades_base = unidad.ratio * cantidad


            id_unidadmedida_referencia = request.POST['id_unidad_referencia']
            cantidad_max = request.POST['cantidad_max']
            id_producto = request.POST['id_producto']
            id_origen = request.POST['id_origen']
            id_profileposition = request.POST['id_profileposition']
            producto  = get_object_or_404(Producto, pk=id_producto)
            origen = get_object_or_404(Profile, pk=id_origen)
            profileposition = get_object_or_404(ProfilePosition, pk=id_profileposition)
            unidadmedida_referencia  = get_object_or_404(UnidadMedida, pk=id_unidadmedida_referencia)
            unidad_enviada = form.cleaned_data['unidad']

            creador  = return_profile(request.user.username, "STAFF")

            dicc_movimiento = {
                    "vale":obj, 
                    "tipo_movimiento":obj.tipo_movimiento,
                    "fecha_movimiento":obj.fecha_vale,                

                    "origen":origen,
                    "producto":producto,                    

                    "unidad": form.cleaned_data['unidad'],
                    "cantidad":cantidad,
                    "observacion":form.cleaned_data['observacion'],
                    "destino":form.cleaned_data['destino'],

                    "creador":creador
            }

            if unidadmedida_referencia.categoria == unidad_enviada.categoria:
                pass
                #messages.add_message(request, messages.SUCCESS, 'La unidad de medida enviada, es correcta.')
            else:
                messages.add_message(request, messages.ERROR, 'La unidad de medida enviado, no corresponde con el producto')
                return HttpResponseRedirect(reverse('salida_general_add', args=[obj.id]))    

            if float(cantidad_en_unidades_base) <= float(cantidad_max): ## extra validacion, solo puede sacarse una cantidad menor o igual a lo existente
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
def entrada_general_erase_movimiento(request, vale_id, movimiento_id):
    
    obj_vale = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    obj_movimiento = get_object_or_404(MovimientoGeneral, pk=movimiento_id)
    for productoexactprofileposition in obj_movimiento.le_positions():
        productoexactprofileposition.delete()
    obj_movimiento.delete()

    messages.add_message(request, messages.SUCCESS, 'Se borra movimiento')
    return HttpResponseRedirect(reverse('entrada_general_add', args=[obj_vale.id]))


@login_required
def general_impresion(request, vale_id):
    context = {}
    obj = get_object_or_404(ValeAlmacenGeneral, pk=vale_id)
    context['vale'] = obj
    return render(request, 'formato_general.html', context)
