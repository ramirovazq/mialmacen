from datetime import datetime

def gastos_filter(request, registros):

    concepto = request.POST.get('concepto', False)

    fecha_gasto_inicio = request.POST.get('fecha_gasto_inicio', '')
    fecha_gasto_fin = request.POST.get('fecha_gasto_fin', '')

    categoria = request.POST.get('categoria', False)
    perdida = request.POST.get('perdida', False)


    if concepto:
        registros = registros.filter(concepto__icontains=concepto)

    if fecha_gasto_inicio:
        registros = registros.filter(fecha__gte=datetime.strptime(fecha_gasto_inicio, '%d-%m-%Y'))
    if fecha_gasto_fin:
        registros = registros.filter(fecha__lte=datetime.strptime(fecha_gasto_fin, '%d-%m-%Y'))

    if categoria:
        registros = registros.filter(categoria__id=categoria)

    perdida_true = perdida in ["on"]
    if perdida_true:
        registros = registros.filter(perdida=False)

    return registros
