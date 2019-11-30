from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse

from .forms import *
from .models import *
from .utils import *
from shared.utils import compare_with_db

@login_required
def profiles(request):
    context = {}
    p = Profile.objects.all().order_by('-id')
    
    paginator = Paginator(p, settings.ITEMS_PER_PAGE) # Show 5 profiles per page
    page = request.GET.get('page')
    p = paginator.get_page(page)

    context["profiles"] = p
    return render(request, 'profiles.html', context)    

@login_required(redirect_field_name='next')
@group_required(settings.GROUP_NAME_ADMINS)
def bodega_add(request):
    context = {}
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            profile = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de forma exitosa la bodega: {}'.format(profile.user.username))
            return HttpResponseRedirect(reverse('profiles'))
    else:
        form = BodegaForm()

    context["form"] = form
    return render(request, 'add.html', context)

@login_required(redirect_field_name='next')
@group_required(settings.GROUP_NAME_ADMINS)
def economico_add(request):
    context = {}
    if request.method == 'POST':
        form = EconomicoForm(request.POST)
        if form.is_valid():
            profile = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de forma exitosa un económico: {}'.format(profile.user.username))
            return HttpResponseRedirect(reverse('profiles'))
    else:
        form = EconomicoForm()

    context["form"] = form
    return render(request, 'economico_add.html', context)


@login_required(redirect_field_name='next')
@group_required(settings.GROUP_NAME_ADMINS)
def proveedor_add(request):
    context = {}
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            profile = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de forma exitosa el proveedor: {}'.format(profile.user.username))
            return HttpResponseRedirect(reverse('profiles'))
    else:
        form = ProveedorForm()

    context["form"] = form
    return render(request, 'proveedor_add.html', context)


@login_required(redirect_field_name='next')
@group_required(settings.GROUP_NAME_ADMINS)
def producto_add(request):
    context = {}
    if request.method == 'POST':

        form = ProductoForm(request.POST)
        if form.is_valid(): # not empty, and at least 2 characters
            #profile = form.save()
            messages.add_message(request, messages.INFO, 'Verifica las coincidencias')
            nombre_validado = form.cleaned_data['nombre']
            respuesta, lista_posible = compare_with_db(nombre_validado.upper(), numero_porcentaje_parecido=.3)
            context["lista"] = lista_posible
            context["nombre_validado"] = nombre_validado.upper()
            instancia = Producto(nombre=nombre_validado.upper())
            formdos = ProductoValidadoForm(instance= instancia)
            context["form_validado"] = formdos
    else:
        form = ProductoForm()

    context["form"] = form
    return render(request, 'producto_add.html', context)


@login_required(redirect_field_name='next')
@group_required(settings.GROUP_NAME_ADMINS)
def producto_confirma_add(request):
    context = {}
    if request.method == 'POST':
        form = ProductoValidadoForm(request.POST)
        if form.is_valid(): # not empty, and at least 2 characters
            nuevo_producto = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se agregó de forma correcta el producto: {}'.format(nuevo_producto.nombre))
        else:
            messages.add_message(request, messages.ERROR, 'Error, verifica')
            for e in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[e])
    return HttpResponseRedirect(reverse('producto_add'))
