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
        Se encarga de cargar los productos, de productos_no_encontrados__en_entradas__verify
        '''

        with open(settings.BASE_DIR + '/load_init/productos_no_encontrados__en_entradas__verify.csv') as csvfile_in:
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
                    #numero_de_parte      = row[0].strip()
                    producto_match       = row[5].strip() # ENTRADA SALIDA ## mayusculas
                    producto_match      = producto_match.upper() # ENTRADA SALIDA ## mayusculas

                    producto_original      = row[6].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper()

                    if producto_match != '':
                        numero_productos += 1

                        try:
                            producto = Producto.objects.get(nombre=producto_original)
                            msg = 'True {}'.format(producto_original)
                            existe_producto += 1
                            #msg = ''
                            self.stdout.write(self.style.SUCCESS(msg))
                        except Producto.DoesNotExist:
                            #msg = "no encuentra producto ;("
                            producto, msg = crea_producto(producto_original)
                            self.stdout.write(self.style.ERROR(msg))
                            no_existe_producto += 1
                        except MultipleObjectsReturned:
                            self.stdout.write(self.style.ERROR("MULTIPLES PRODUCTOS RETORNADOS .............................................."))

            self.stdout.write(self.style.SUCCESS('Resumen numero productos: ..... {}'.format(numero_productos)))    # 364
            self.stdout.write(self.style.SUCCESS('Productos encontrados: ........ {}'.format(existe_producto)))     # 171
            self.stdout.write(self.style.SUCCESS('Productos no existen: ......... {}'.format(no_existe_producto)))  # 193
                    