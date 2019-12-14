from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


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


            existe_proveedor = 0
            no_existe_proveedor = 0
            notas = 0
            todos = 0
            lista_no_encontrados = []

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

                    proveedor_slug = slugify(proveedor)
                    proveedor_mayus = proveedor_slug.upper()
                    #profile = return_profile(proveedor_mayus, tipo="PROVEEDOR")


                    try:
                        u = User.objects.get(username=proveedor_mayus)
                        #self.stdout.write(self.style.SUCCESS(":) {}".format(u.username)))
                        existe_proveedor += 1
                    except User.DoesNotExist:
                        #self.stdout.write(self.style.ERROR(":( {}".format(proveedor_mayus)))
                        if "NOTA" in  proveedor_mayus:
                            notas += 1
                        else:
                            lista_no_encontrados.append(proveedor_mayus)
                            no_existe_proveedor += 1
                            return_profile(proveedor_mayus, tipo="PROVEEDOR")
                        #pass_new = "{}{}".format(random_string_generator(), randint(0, 100))
                        #u = User.objects.create_user(username, '{}@fletesexpress.com.mx'.format(username), pass_new)
            lista_no_encontrados.sort()
            for x in lista_no_encontrados:
                print(x)




            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('Resumen'))                                              
            self.stdout.write(self.style.SUCCESS('Proveedor: .......... existen    :{}'.format(existe_proveedor)))    # 1182
            self.stdout.write(self.style.SUCCESS('Proveedor ........... no existen :{}'.format(no_existe_proveedor))) #   45
            self.stdout.write(self.style.SUCCESS('Notas .......................... :{}'.format(notas)))               #   42
            self.stdout.write(self.style.SUCCESS('Todos ..........................  {}'.format(todos)))              #  1269
