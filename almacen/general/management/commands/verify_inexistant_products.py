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

class Command(BaseCommand):
    help = 'Load init productos from CSV, for almacen general.'
    def handle(self, *args, **options):
        '''
        lee el archivo verificar_revisado.csv (tiene todos los productos no encontrados)
        de ahi, se hacen 3 agrupaciones
        a) los que se encuentran directos en la db existe_producto
        b) los que no encuentra en la db no_existe_producto 
        c) si llegara a haber un producto repetido, en la tabla de productos 
        '''

        with open(settings.BASE_DIR + '/load_init/verificar_revisado.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')

            # Lllanta
            numero_productos = 0     #595
            existe_producto = 0
            no_existe_producto = 0


            for indice, row in enumerate(readCSV):
                if indice == 0:
                    nombre_title         = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    numero_parte_title     = row[1].strip() # ENTRADA SALIDA ## mayusculas
                else: # quit name of column
                    numero_de_parte      = row[0].strip()
                    producto_match       = row[1].strip() # ENTRADA SALIDA ## mayusculas
                    producto_match      = producto_match.upper() # ENTRADA SALIDA ## mayusculas

                    producto_original      = row[2].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper()

                    if producto_match != '':
                        numero_productos += 1

                        try:
                            producto = Producto.objects.get(nombre=producto_original)
                            msg = 'True {}'.format(producto_original)
                            msg = crea_numero_de_parte(producto, numero_de_parte, msg)
                            existe_producto += 1
                            #msg = ''
                            self.stdout.write(self.style.SUCCESS(msg))
                        except Producto.DoesNotExist:
                            producto, msg = crea_producto(producto_original)
                            if producto:
                                msg = crea_numero_de_parte(producto, numero_de_parte, msg)
                            self.stdout.write(self.style.ERROR(msg))
                            no_existe_producto += 1
                        except MultipleObjectsReturned:
                            self.stdout.write(self.style.ERROR("MULTIPLES PRODUCTOS RETORNADOS .............................................."))

            self.stdout.write(self.style.SUCCESS('Resumen numero productos: ..... {}'.format(numero_productos)))    #595
            self.stdout.write(self.style.SUCCESS('Productos encontrados: ........ {}'.format(existe_producto)))     #335
            self.stdout.write(self.style.SUCCESS('Productos no existen: ......... {}'.format(no_existe_producto)))  #260
                    