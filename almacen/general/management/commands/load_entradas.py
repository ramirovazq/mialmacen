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
    help = 'Load entradas from CSV, to almacen general.'
    def handle(self, *args, **options):
        '''
        lee el archivo entradas.csv
        de ahi, se 
        '''
        no_match_productos = False

        with open(settings.BASE_DIR + '/load_init/entradas.csv') as csvfile_in, open(settings.BASE_DIR + '/load_init/productos_no_encontrados__en_entradas.csv', 'w') as csvfile_out_sinmatch:
            readCSV = csv.reader(csvfile_in, delimiter=';')

            writer_sin_match = csv.writer(csvfile_out_sinmatch, delimiter=";")
            writer_sin_match.writerow(['fecha', 'proveedor', 
                        'numero_folio', 'numero_parte', 
                        'cantidad', 'producto_original', '', '',
                        'precio_unitario', 'subtotal',
                        'iva', 'total', 'tractor'])


            existe_producto = 0
            no_existe_producto = 0
            repetidos = 0
            numero_de_parte = None
            todos = 0

            for indice, row in enumerate(readCSV):
                if indice != 0: #nos saltmamos la cabecera
                    todos += 1

                    fecha                  = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    proveedor              = row[1].strip()

                    numero_folio           = row[2].strip() # ENTRADA SALIDA ## mayusculas
                    numero_parte           = row[3].strip() # ENTRADA SALIDA ## mayusculas

                    cantidad               = row[4].strip()

                    producto_original      = row[5].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas

                    precio_unitario        = row[6].strip()
                    subtotal               = row[7].strip()
                    iva                    = row[8].strip()
                    total                  = row[9].strip()

                    tractor                = row[10] # ENTRADA SALIDA ## mayusculas

                    try:
                        producto = Producto.objects.get(nombre=producto_original)
                        msg = 'True {}'.format(producto_original)
                        #msg = 'True'
                        self.stdout.write(self.style.SUCCESS(msg))
                        existe_producto += 1
                    except Producto.DoesNotExist:
                        msg = 'False'
                        # no_existe_producto += 1

                        parte_uno_list = NumeroParte.objects.filter(numero_de_parte=numero_parte)
                        # parte_dos_list = NumeroParte.objects.filter(numero_de_parte=numero_parte_dos)

                        if ((len(parte_uno_list) > 0)):
                            msg = "True"
                            self.stdout.write(self.style.SUCCESS(msg))
                            existe_producto += 1
                        else: 
                            self.stdout.write(self.style.ERROR(msg))
                            no_existe_producto += 1

                            if no_match_productos:
                                writer_sin_match.writerow([fecha, proveedor,
                                        numero_folio, numero_parte, 
                                        cantidad, producto_original,
                                        '', '', 
                                        precio_unitario, subtotal, 
                                        iva, total, tractor])


                                respuesta, lista_posibles = compare_with_db(producto_original, numero_porcentaje_parecido=.4)
                                if respuesta:
                                    for x in lista_posibles:
                                        #print("{} -- {} -- {} ---- {}".format(numero_de_parte, x[0], x[1], x[2]))
                                        writer_sin_match.writerow(['', '', '', '', '', '', x[2], str(x[0])])


                        
                    except MultipleObjectsReturned:
                        repetidos += 1
                        msg = 'Producto repetido ............................................. {}'.format(producto_original)
                        self.stdout.write(self.style.ERROR(msg))

            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('Resumen'))                                              
            self.stdout.write(self.style.SUCCESS('Productos: .......... existen    :{}'.format(existe_producto)))    # 210 ..... 583
            self.stdout.write(self.style.SUCCESS('Productos ........... no existen :{}'.format(no_existe_producto))) # 672 ..... 299
            self.stdout.write(self.style.SUCCESS('Productos ........... repetidos  :{}'.format(repetidos)))          # 0
            self.stdout.write(self.style.SUCCESS('Todos ..........................  {}'.format(todos)))              # 882 ..... 882
