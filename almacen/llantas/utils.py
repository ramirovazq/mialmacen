from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User

from persona.models import Profile, Tipo, Position
from llantas.models import Llanta, LlantaBasura
from general.models import NumeroParte, Producto

from random import randint
from datetime import datetime

import string
import random
import textdistance as textd
import csv

def return_position(nombre="", padre=None):
    if not padre:
        return Position.objects.create(name=nombre)
    return Position.objects.create(name=nombre, parent=padre)


def return_folio_str(number, places=5):
    '''
    redibe un enter, number
    devuelve en str ese entero lleno con ceros
    '''
    n_str = "{}".format(number)
    return n_str.zfill(places)

def concatenate_folio(number, folio_xls, folio_nota):
    answer = ""    
    folio_tmp = return_folio_str(number)
    
    if folio_xls != "":
        answer = "{}-{}".format(folio_tmp, folio_xls)
    else:
        answer = "{}".format(folio_tmp)
    

    if folio_nota:
        answer = "{}-{}".format(answer, folio_nota)
    return answer

def concatenate_folio_(folio_xls, folio_nota):
    answer = ""    
    
    if folio_xls != "":
        answer = "{}".format(folio_xls)    

    if answer:    
        if folio_nota:
            answer = "{}-{}".format(answer, folio_nota)
    elif folio_nota:
        answer = "{}".format(folio_nota)
        
    return answer


def proveedor_desconocido():
    return return_profile("DESCONOCIDO", tipo="PROVEEDOR")

def proveedor_normalize(cadena_proveedor):
    '''
    recibe una cadena con el nombre del proveedor
    la convierta en un slug
    y finalmente la transforma a mayusculas
    '''
    proveedor = cadena_proveedor.strip() # quita espacios en blanco
    proveedor_slug = slugify(proveedor)
    proveedor_mayus = proveedor_slug.upper()
    return proveedor_mayus

def devuelve_objeto_proveedor(proveedor_mayus):
    '''
    return Profile or False or "NOTA"
    busca devolver el Profile del proveedor 
    sino lo encuentra, devuelve False
    y si es una nota, devulve la cadena NOTA
    '''
    #print(proveedor_mayus)

    t, band = Tipo.objects.get_or_create(nombre="PROVEEDOR")

    if "NOTA" in proveedor_mayus:
        return False

    try:
        u = User.objects.get(username=proveedor_mayus)
        p = Profile.objects.get(user=u, tipo=t)
        return p
    except Profile.DoesNotExist:
        return False
    except User.DoesNotExist:
        return False


def busqueda_en_archivo_diccionario(producto_a_buscar):
    with open(settings.BASE_DIR + '/load_init/productos_no_encontrados__en_entradas__verify.csv') as csvfile_in:
        readCSV = csv.reader(csvfile_in, delimiter=';')

        for indice, row in enumerate(readCSV):
            if indice == 0:
                nombre_title         = row[0].strip() # ENTRADA SALIDA ## mayusculas
                numero_parte_title     = row[1].strip() # ENTRADA SALIDA ## mayusculas
            else: # quit name of column

                producto_original       = row[5].strip() # ENTRADA SALIDA ## mayusculas
                producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas

                producto_final      = row[6].strip() # ENTRADA SALIDA ## mayusculas
                producto_final      = producto_final.upper()

                if producto_original != '':
                    if producto_original == producto_a_buscar:
                        return producto_final




def compare_with_db(nombre_producto, numero_porcentaje_parecido=.5):
    '''
    esta funcion compara una cadena nombre_producto
    contra todas los productos de la db
    si el parecido es mayor o igual a numero_porcentaje_parecido, se agrega a la lista de parecidos
    finralmente se regresa la lista de parecidos, pero ordenados por los mas parecidos hasta arriba
    '''
    respuesta = False
    lista = []
    for productodb in Producto.objects.all():                                                                                                                                                    
        numero = textd.levenshtein.normalized_similarity(productodb.nombre, nombre_producto) 
        if numero >= numero_porcentaje_parecido:                                                         
            lista.append((numero, nombre_producto, productodb.nombre))
            respuesta = True

    lista_sorted = sorted(lista, key=lambda x: x[0], reverse=True)
    return respuesta, lista_sorted


def crea_numero_de_parte(producto, numero_de_parte, msg=""):
    if numero_de_parte != "":
        obj, created= NumeroParte.objects.get_or_create(producto=producto, numero_de_parte=numero_de_parte)
        if created:
            msg = msg + " :D num_parte"
        else:
            msg = msg + " :l existia num_parte"
    return msg

def crea_producto(producto, msg=""):
    obj = None
    if producto != "":
        obj, created= Producto.objects.get_or_create(nombre=producto)
        if created:
            msg = msg + "producto :D creado"
        else:
            msg = msg + "producto :l ya existia"
    return obj, msg


def devuelve_llanta(marca, medida, posicion, status, dot):
    llanta_already_exist = False
    llantas = Llanta.objects.filter(marca=marca, medida=medida, posicion=posicion, status=status, dot=dot)
    if len(llantas) > 0:
        llanta_already_exist = True
        llanta = llantas[0]
    else:
        llanta = Llanta.objects.create(marca=marca, medida=medida, posicion=posicion, status=status, dot=dot)
    return llanta, llanta_already_exist


def devuelve_llanta_basura(marca, medida, posicion, status, dot):
    llanta_already_exist = False
    dict_llanta_basura = {}
    if marca:
        dict_llanta_basura["marca"] = marca
    if medida:
        dict_llanta_basura["medida"] = medida
    if posicion:
        dict_llanta_basura["posicion"] = posicion
    if status:
        dict_llanta_basura["status"] = status
    if dot:
        dict_llanta_basura["dot"] = dot

    llantas = LlantaBasura.objects.filter(**dict_llanta_basura)
    if len(llantas) > 0:
        llanta_already_exist = True
        llanta = llantas[0]
    else:
        llanta = LlantaBasura.objects.create(**dict_llanta_basura)
    return llanta_already_exist, llanta


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
    '''
    return user
    busca encontrar un User
    sino lo encuentra, simplemente lo crea y lo devuelve
    '''
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        pass_new = "{}{}".format(random_string_generator(), randint(0, 100))
        u = User.objects.create_user(username, '{}@fletesexpress.com.mx'.format(username), pass_new)
    return u

def return_existent_user(username):
    '''
    return user
    busca encontrar un User
    sino lo encuentra, simplemente lo crea y lo devuelve
    '''
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return False, None
    return True, u


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
    '''
    return Profile
    busca encontrar un Profile, desde un user
    sino lo encuentra, simplemente lo crea y lo devuelve
    '''
    tipo, flag = Tipo.objects.get_or_create(nombre=tipo)
    try:
        p = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        p = Profile.objects.create(user=user, tipo=tipo)
    return p

def return_profile(username, tipo="STAFF"):
    '''
    return Profile
    busca encontrar el User usando el username, sino crea el User
    con ese usar, busca encontrar el Profile, sino lo crea el Profile
    '''
    u = return_or_create_user(username)
    return create_profile(u, tipo)

def return_existent_profile(usuario, tipo="STAFF"):
    # u = return_existent_user(username)
    try:
        tipo = Tipo.objects.get(nombre=tipo)
    except Tipo.DoesNotExist:
        return False, None
    try:
        p = Profile.objects.get(user=usuario)
    except Profile.DoesNotExist:
        return False, None
    return True, p



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
