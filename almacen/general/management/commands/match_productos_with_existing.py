from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone

from llantas.utils import *
from llantas.models import *
from general.models import *
from persona.models import *

import csv, os, datetime
import textdistance as textd

class Command(BaseCommand):
    help = 'Load init productos from CSV, for almacen general.'
    def handle(self, *args, **options):
        '''
        Toma el archivo productos_no_encontrados.csv  y 
        producce verificar.csv que es donde busca articulos que tengan igual o mas del 50% de coincidencia
        tambien produce sinmatch.csv, donde vienen articulos que no encontraron coincidencia, se creen que son nuevos en verdad
        '''
        def crea_numero_de_parte(producto, numero_de_parte, msg):
            if numero_de_parte != "":
                obj, created= NumeroParte.objects.get_or_create(producto=producto, numero_de_parte=numero_de_parte)
                if created:
                    msg = msg + " :D num_parte"
                else:
                    msg = msg + " :l existia num_parte"
            return msg

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


        with open(settings.BASE_DIR + '/load_init/productos_no_encontrados.csv') as csvfile_in, open(settings.BASE_DIR + '/load_init/verificar.csv', 'w') as csvfile_out, csvfile_in, open(settings.BASE_DIR + '/load_init/sinmatch.csv', 'w') as csvfile_out_sinmatch:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            lines = list(readCSV)

            writer_sin_match = csv.writer(csvfile_out_sinmatch, delimiter=";")
            writer_sin_match.writerow(['Producto sin match', 'numero_de_parte'])

            writer = csv.writer(csvfile_out, delimiter=";")
            writer.writerow(['Numer_de_parte', 'Producto con match', 'Posibles', 'porcentaje'])
   
            total = 0
            encuentra_match = 0
            repetidos = 0
            sinmatch = 0
            avoid_repetitions = {} 

            for indice, row in enumerate(lines):
                if indice == 0:
                    nombre_title         = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    numero_parte_title     = row[1].strip() # ENTRADA SALIDA ## mayusculas
                else: # quit name of column
                    producto_original      = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas
                    numero_de_parte      = row[1].strip()
            

                    total += 1
                    
                    respuesta, lista_posibles = compare_with_db(producto_original)
                    if respuesta:
                        encuentra_match += 1
                        writer.writerow([numero_de_parte, producto_original, '', ''])
                        for x in lista_posibles:
                            print("{} -- {} -- {} ---- {}".format(numero_de_parte, x[0], x[1], x[2]))
                            writer.writerow(['', '', x[2], str(x[0])])
                    else:
                        sinmatch += 1
                        writer_sin_match.writerow([producto_original, numero_de_parte])

            print(" ")        
            print(" ")        
            print("RESUMEN")
            print(" ................... repetidos: {}".format(repetidos))       ## 116.       0
            print(" .........  encuentra posibles: {}".format(encuentra_match)) ## 523.     595
            print(" ..................  sin match: {}".format(sinmatch))         ## 220.    264
            print("__________________________________")
            print(" ......................  total: {}".format(total))             ## 859.   859
