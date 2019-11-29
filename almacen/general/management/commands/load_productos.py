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
        lee el archivo articulos_con_numero_de_parte.csv, el original para analisis
        de ahi, se hacen 3 agrupaciones
        a) los que se encuentran directos en la db existe_producto 365. De estos, aqui mismo se crean los numeros de parte sino existen.
        b) los que no encuentra en la db no_existe_producto 859 etos solo son impresos, y por ello se pueden llevar a un csv
        c) si llegara a haber un producto repetido, en la tabla de productos (se evita al hacerlo unique en la tabla de productos) pero es de tiempos pasados
        '''
        def crea_numero_de_parte(producto, numero_de_parte, msg):
            if numero_de_parte != "":
                obj, created= NumeroParte.objects.get_or_create(producto=producto, numero_de_parte=numero_de_parte)
                if created:
                    msg = msg + " :D num_parte"
                else:
                    msg = msg + " :l existia num_parte"
            return msg

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
                    numero_de_parte      = row[1].strip()

                    try:
                        producto = Producto.objects.get(nombre=producto_original)
                        msg = 'True {}'.format(producto_original)
                        msg = crea_numero_de_parte(producto, numero_de_parte, msg)
                        existe_producto += 1
                        #msg = ''
                        self.stdout.write(self.style.SUCCESS(msg))
                    except Producto.DoesNotExist:
                        if numero_de_parte:
                            msg = '{};{}'.format(producto_original, numero_de_parte)
                        else:
                            msg = '{};'.format(producto_original)
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
