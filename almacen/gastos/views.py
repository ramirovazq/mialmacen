from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now as d_utils_now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from .forms import GastoForm, FilterGastoForm
from .models import Gasto
from .utils import gastos_filter
# Create your views here.

@login_required
def registro(request):

    hoy = d_utils_now()
    fecha_hoy = hoy.strftime("%d-%m-%Y")    
    initial_data = {
        'fecha': fecha_hoy, 
        'user': request.user,
        'perdida': True
    }
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, 
                'Registro guardado exitosamente'
            )
            return HttpResponseRedirect(reverse('registro'))
        else:
            messages.add_message(
                request, 
                messages.ERROR, 
                'Verifica el formulario'
            )
    else:
        form = GastoForm(initial=initial_data)
    return render(request, 'registro.html', {'form': form})

@login_required
def registros(request):
    context = {}
    m = Gasto.objects.all().order_by('-fecha')
    
    if request.method == 'POST':
        form = FilterGastoForm(request.POST)
        if form.is_valid():
            m = gastos_filter(request, m)            
    else:
        form = FilterGastoForm()
    
    context["form"] = form
    context["movimientos_count"] = m.count()
    paginator = Paginator(m, settings.ITEMS_PER_PAGE) # Show 5 profiles per page

    page = request.GET.get('page')
    m = paginator.get_page(page)

    context["registros"] = m
    return render(request, 'registros.html', context)    
