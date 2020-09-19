from datetime import datetime

def gastos_filter(request, registros):

    concepto = request.POST.get('concepto', False)

    fecha_gasto_inicio = request.POST.get('fecha_gasto_inicio', '')
    fecha_gasto_fin = request.POST.get('fecha_gasto_fin', '')

    categoria = request.POST.get('categoria', False)
    perdida = request.POST.get('perdida', False)


    ### new ... INICIO
    #if tipo_movimiento:
    #  registros = registros.filter(vale__tipo_movimiento=tipo_movimiento)

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
        print("perdida")
        print(perdida)
        registros = registros.filter(perdida=False)
        #registros = registros.filter(perdida=perdida)

    '''
    if fecha_creacion_inicio:
        print("uno")
        registros = registros.filter(date_created__gte=datetime.strptime(fecha_creacion_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if fecha_creacion_fin:
        print("dos ....")
        registros = registros.filter(date_created__lte=datetime.strptime(fecha_creacion_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))
    if no_folio:
        registros = registros.filter(vale__no_folio__icontains=no_folio)

    if origen:
        registros = registros.filter(origen__id=origen)
    if destino:
        registros = registros.filter(destino__id=destino)
    if marca:
        registros = registros.filter(marca__id=marca)
    if medida:
        registros = registros.filter(medida__id=medida)
    if posicion:
        registros = registros.filter(posicion__id=posicion)
    if status:
        registros = registros.filter(status__id=status)

    if dot:
        registros = registros.filter(dot__icontains=dot)
    if creador:
        registros = registros.filter(creador__id=creador)


    '''
    '''

    if producto:
      registros = registros.filter(producto__icontains=producto)

    if compania:
      registros = registros.filter(compania__icontains=compania)

    if propietario:
      registros = registros.filter(propietario__icontains=propietario)

    if detalle:
      registros = registros.filter(detalle__icontains=detalle)



    if ultima_actualizacion_inicio:
      registros = registros.filter(ultima_actualizacion__gte=datetime.strptime(ultima_actualizacion_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if ultima_actualizacion_fin:
      registros = registros.filter(ultima_actualizacion__lte=datetime.strptime(ultima_actualizacion_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))

    if fecha_programada_inicio:
      registros = registros.filter(fecha_programada__gte=datetime.strptime(fecha_programada_inicio+'00:00:00', '%d-%m-%Y%H:%M:%S'))
    if fecha_programada_fin:
      registros = registros.filter(fecha_programada__lte=datetime.strptime(fecha_programada_fin+'23:59:59', '%d-%m-%Y%H:%M:%S'))
    '''
    return registros
