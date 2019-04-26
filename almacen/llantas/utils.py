from django.contrib.auth.models import User
from persona.models import Profile, Tipo
from llantas.models import Llanta
from random import randint
from datetime import datetime
import string
import random

def devuelve_llanta(marca, medida, posicion, status, dot):
    llanta_already_exist = False
    llantas = Llanta.objects.filter(marca=marca, medida=medida, posicion=posicion, status=status, dot=dot)
    if len(llantas) > 0:
        llanta_already_exist = True
        llanta = llantas[0]
    else:
        llanta = Llanta.objects.create(marca=marca, medida=medida, posicion=posicion, status=status, dot=dot)
    return llanta, llanta_already_exist


def agrupacion_dots(lista_dots):
    '''
    {'3218': 2, '3628': 1, '3618': 2} la llave es el dot, y el valor el numero de veces que esta
    '''
    dicc = {}
    for x in lista_dots:
        if x not in dicc.keys():
            dicc[x] = 1
        else:
            dicc[x] = dicc[x] + 1
    return dicc

def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def return_or_create_user(username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        pass_new = "{}{}".format(random_string_generator(), randint(0, 100))
        u = User.objects.create_user(username, '{}@fletesexpress.com.mx'.format(username), pass_new)
    return u

def return_permisionario(username):
    
    try:
        tipo_permisionario = Tipo.objects.get(nombre="PERMISIONARIO")
        u = User.objects.get(username=username)
        profile = Profile.objects.get(user=u, tipo=tipo_permisionario)
    except User.DoesNotExist:
        u = None
        profile = None        
    except Profile.DoesNotExist:
        u = None
        profile = None
    except Tipo.DoesNotExist:
        u = None
        profile = None

    return profile



def create_profile(user, tipo="STAFF"):

    tipo, flag = Tipo.objects.get_or_create(nombre=tipo)
    try:
        p = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        p = Profile.objects.create(user=user, tipo=tipo)
    return p

def return_profile(username, tipo="STAFF"):
    u = return_or_create_user(username)
    return create_profile(u, tipo)

def split_list(lista):
    return [(x[0].split("__"), x[1])for x in lista]

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
