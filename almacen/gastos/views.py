from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now as d_utils_now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import GastoForm
# Create your views here.

@login_required
def registro(request):

    hoy = d_utils_now()
    fecha_hoy = hoy.strftime("%d-%m-%Y")    
    initial_data = {
        'fecha': fecha_hoy, 
        'user': request.user
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