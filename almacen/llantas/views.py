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

from datetime import datetime

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .utils import *
from .models import *
from persona.models import Profile, Tipo
from .forms import FilterForm, FilterMovimientoForm, ValeForm, SearchSalidaForm, MovimientoSalidaForm, EntradaForm, NewLlantaForm, ImportacioMovimientosForm, AdjuntoValeForm, ProfileSearchForm
from .render_to_XLS_util import render_to_xls, render_to_csv, render_to_xls_inventario
from .serializers import ValeSerializer, LlantaSerializer, ProfileSerializer, MovimientoSerializer

## curl -X GET http://127.0.0.1:8000/api/v0/vale/ -H 'Authorization: Token ABCDEF343434342234234KMLMKMLKM'
class MovimientoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Movimiento.objects.all().order_by('-date_created')
    serializer_class = MovimientoSerializer


class ValeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Vale.objects.all().order_by('-fecha_created')
    serializer_class = ValeSerializer


    def perform_create(self, serializer):
        if not 'no_folio' in serializer.validated_data.keys():
            vale = serializer.save(no_folio=Vale.siguiente_folio())
        else:
            vale = serializer.save()


class LlantaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Llanta.objects.all()
    serializer_class = LlantaSerializer


class EconomicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    obj_tipo, bandera = Tipo.objects.get_or_create(nombre="ECONOMICO")
    queryset = Profile.objects.filter(tipo=obj_tipo)
    serializer_class = ProfileSerializer


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
        if 'profile' in request.POST: ### cual formulario se envio

            form = SearchSalidaForm()
            form_profile = ProfileSearchForm(request.POST)

            if form_profile.is_valid():
                profile = form_profile.cleaned_data['profile']
                movimientos_entrada = Movimiento.entradas()
                movimientos_entrada_permisionario = movimientos_entrada.filter(permisionario=profile)

                id_llanta = movimientos_entrada_permisionario.values_list('llanta__id')
                unique_id_llanta = list(set(id_llanta))
                lista_unique_id_llanta = [x[0] for x in unique_id_llanta]

                messages.add_message(request, messages.INFO, 'Búsqueda por permisionario: {}'.format(profile))
                search = Llanta.objects.filter(id__in=lista_unique_id_llanta)


        else: ##
            form = SearchSalidaForm(request.POST)
            form_profile = ProfileSearchForm()
            if form.is_valid():
                search_filtrado = []

                dicc_llanta = {}
                dot = form.cleaned_data['dot']
                marca = form.cleaned_data['marca']
                medida = form.cleaned_data['medida']
                posicion = form.cleaned_data['posicion']
                status = form.cleaned_data['status']

                if dot:
                    dicc_llanta['dot__icontains'] = dot
                if marca:
                    dicc_llanta['marca'] = marca
                if medida:
                    dicc_llanta['medida'] = medida
                if posicion:
                    dicc_llanta['posicion'] = posicion
                if status:
                    dicc_llanta['status'] = status

                if dicc_llanta.keys():
                    messages.add_message(request, messages.INFO, 'Búsqueda por: {}'.format(dicc_llanta))
                    search = Llanta.objects.filter(**dicc_llanta)
                else:
                    messages.add_message(request, messages.INFO, 'Selecciona almenos un criterio de búsqueda.')

    else:
        form = SearchSalidaForm()
        form_profile = ProfileSearchForm()

    context["form_profile"] = form_profile
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
        llantas = llantas.order_by('marca__nombre')


    if export:
        return render_to_xls_inventario(
                queryset=llantas,
                filename="export_inventario.xls"
            )                


    context['orden'] = orden        
    context['llantas'] = llantas
    context['url_export'] = url_export

    return render(request, 'actual.html', context)    

'''
@login_required
def salidas(request):
    context = {}
    v = Vale.objects.filter(tipo_movimiento__nombre='SALIDA').order_by('-fecha_vale', '-no_folio')
    
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    return render(request, 'vales.html', context)    

@login_required
def entradas(request):
    context = {}
    v = Vale.objects.filter(tipo_movimiento__nombre='ENTRADA').order_by('-fecha_vale', '-no_folio')
    
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    context["action"] = "entrada"
    return render(request, 'vales.html', context)    
'''

@login_required
def vales(request):
    context = {}
    action = request.GET.get("tipo", "ENTRADA")
    
    if action:
        action = action.upper()

    v = Vale.objects.filter(tipo_movimiento__nombre=action, vale_llantas=True).order_by('-fecha_vale', '-no_folio')
    context["vales_count"] = v.count()


    paginator = Paginator(v, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    v = paginator.get_page(page)

    context["vales"] = v
    context["action"] = action
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

            dicc_movimiento = {
                    "vale":obj, 
                    "tipo_movimiento":obj.tipo_movimiento,
                    "fecha_movimiento":obj.fecha_vale,                
                    "origen":origen,
                    "destino":form.cleaned_data['destino'],
                    "llanta":llanta,
                    "cantidad":form.cleaned_data['cantidad'],
                    "observacion":form.cleaned_data['observacion'],
                    "creador":creador
            }
            nombre_permisionario = request.POST['nombre_permisionario']
            permisionario = return_permisionario(nombre_permisionario)
            if permisionario:
                dicc_movimiento["permisionario"] = permisionario
                nombre_permisionario = permisionario.user.username
            else:
                nombre_permisionario = nombre_permisionario

            dicc_ubicaciones = llanta.total_ubicaciones_detail()

            cantidad_en_ubicacion = dicc_ubicaciones[origen.user.username][nombre_permisionario]


            if cantidad <= cantidad_en_ubicacion: ## extra validacion, solo puede sacarse una cantidad menor o igual a lo existente
                m = Movimiento(**dicc_movimiento)
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


@login_required
def llanta_detalle(request, llanta_id):
    context = {}
    llanta = get_object_or_404(Llanta, id=llanta_id)

    

    context["llanta"] = llanta
    
    return render(request, 'llanta.html', context)    


@login_required
def vale_erase(request, vale_id):
    redirige_entrada = None
    obj_vale = get_object_or_404(Vale, pk=vale_id)
    if len(obj_vale.movimientos()) == 0:
        obj_vale.delete()
        messages.add_message(request, messages.SUCCESS, 'Se borró el Vale')
    else:
        messages.add_message(request, messages.WARNING, 'Este vale tiene movimientos, no se puede borrar.')
    
    
    return HttpResponseRedirect(reverse('vales')+"?tipo="+obj_vale.tipo_movimiento.nombre)


def home_llantas(request):
    return HttpResponseRedirect(reverse('vales'))
