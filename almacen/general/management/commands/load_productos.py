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
        
        with open(settings.BASE_DIR + '/load_init/articulos_con_numero_de_parte.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')

            # Lllanta
            existe_producto = 0
            no_existe_producto = 0


            for indice, row in enumerate(readCSV):
                if indice == 0:
                    nombre_title         = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    numero_parte_title     = row[1].strip() # ENTRADA SALIDA ## mayusculas
                    
                else: # quit name of column

                    producto_original      = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas

                    try:
                        producto = Producto.objects.get(nombre=producto_original)
                        msg = 'True'.format(producto_original)
                        #msg = ""
                        self.stdout.write(self.style.SUCCESS(msg))
                        existe_producto += 1
                    except Producto.DoesNotExist:
                        msg = 'False {}'.format(producto_original)
                        #msg = ""
                        self.stdout.write(self.style.ERROR(msg))
                        no_existe_producto += 1
                    except MultipleObjectsReturned:
                        existe_producto += 1
                        varios = Producto.objects.filter(nombre=producto_original) #.first()
                        overview = ""
                        lista_num_movimientos = []
                        for prod in varios:
                            num_movimientos = len(MovimientoGeneral.objects.filter(producto=prod))
                            overview = overview + "(id: {}, movs {})".format(prod.id, num_movimientos)
                            lista_num_movimientos.append(num_movimientos)
                        repetidos_mucho = set(lista_num_movimientos) == {0}
                        if repetidos_mucho:
                            msg = 'REPETIDOS MUCHO Y SIN MOVS {} True .... varios: {} -- {}'.format(lista_num_movimientos, producto_original, overview)
                        else:
                            msg = '{} True .... varios: {} -- {}'.format(lista_num_movimientos, producto_original, overview)
                        self.stdout.write(self.style.ERROR(msg))

            self.stdout.write(self.style.SUCCESS('Resumen productos: existen {}  no existen {}'.format(existe_producto, no_existe_producto)))
