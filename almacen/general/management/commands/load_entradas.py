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
        busqueda_en_archivo_diccionario_bandera = True

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

            cadena_proveedor_anterior = ""
            vale_anterior = None
            folio_tmp = 0

            tme, tme_flag = TipoMovimiento.objects.get_or_create(nombre="ENTRADA")
            admin_profile   = return_profile("admin", "STAFF")

            for indice, row in enumerate(readCSV):
                if indice != 0: #nos saltmamos la cabecera
                    todos += 1

                    fecha                  = row[0].strip() # ENTRADA SALIDA ## mayusculas
                    f_movimiento           = datetime.datetime.strptime(fecha, "%m/%d/%Y").date()

                    cadena_proveedor       = proveedor_normalize(row[1]) # sin espacios, mayusculas y en slug
                    proveedor              = proveedor_normalize(row[1]) # sin espacios, mayusculas y en slug

                    numero_folio           = row[2].strip() # ENTRADA SALIDA ## mayusculas
                    numero_parte           = row[3].strip() # ENTRADA SALIDA ## mayusculas

                    cantidad               = row[4].strip()

                    producto_original      = row[5].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas

                    precio_unitario        = row[6].strip()
                    subtotal               = row[7].strip()
                    iva                    = row[8].strip()
                    if iva:
                        bandera_iva = True
                    else:
                        bandera_iva = False
                    total                  = row[9].strip()

                    tractor                = row[10] # ENTRADA SALIDA ## mayusculas

                    '''
                    PRODUCTO 
                    busqueda del producto INICIO
                    '''
                    try:
                        producto = Producto.objects.get(nombre=producto_original)
                        #msg = 'True {}'.format(producto_original)
                        #msg = 'True'
                        #self.stdout.write(self.style.SUCCESS(msg))
                        existe_producto += 1
                    except Producto.DoesNotExist:
                        #msg = 'False'
                        # no_existe_producto += 1

                        parte_uno_list = NumeroParte.objects.filter(numero_de_parte=numero_parte)
                        # parte_dos_list = NumeroParte.objects.filter(numero_de_parte=numero_parte_dos)

                        if ((len(parte_uno_list) == 1)): # solo encuentra un numero de parte que coincide
                            existe_producto += 1
                            num_parte_ = parte_uno_list[0]
                            producto = num_parte_.producto

                        elif ((len(parte_uno_list) > 1)): # mas de un numero de parte encontrado
                            #print("#coincidencias: ", len(parte_uno_list),"; #renglon:", indice+1, "; numero parte:", numero_parte, "; producto_original:", producto_original)
                            producto = None
                            repetidos += 1
                        else: 
                            #self.stdout.write(self.style.ERROR(msg)) 
                            # genera un archivo con porcentaje parecido
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

                            # se realiza la busqueda en el archivio diccionario (el que tiene equivalencias: productos_no_encontrados__en_entradas__verify.csv)
                            if busqueda_en_archivo_diccionario_bandera:
                                producto_original_diccionario = busqueda_en_archivo_diccionario(producto_original)
                                try:
                                    producto = Producto.objects.get(nombre=producto_original_diccionario)
                                    existe_producto += 1
                                except Producto.DoesNotExist:
                                    no_existe_producto += 1
                        
                    except MultipleObjectsReturned:
                        repetidos += 1
                        msg = 'Producto repetido ............................................. {}'.format(producto_original)
                        self.stdout.write(self.style.ERROR(msg))
                    '''
                    PRODUCTO 
                    busqueda del producto FIN
                    '''

                    '''
                    PROVEEDOR INI
                    '''
                    obj_proveedor = devuelve_objeto_proveedor(proveedor)
                    folio_nota = ""
                    if not obj_proveedor: # no lo encuentra, es una NOTA
                        obj_proveedor = proveedor_desconocido()
                        folio_nota = "{}".format(proveedor)
                        #print("{} {}".format(obj_proveedor, proveedor))
                    '''
                    PROVEEDOR FIN
                    '''


                    '''
                    VALE NUEVO, O EXISTENTE
                    '''
                    if cadena_proveedor != cadena_proveedor_anterior: # nueva factura
                        cadena_proveedor_anterior = cadena_proveedor
                        folio_tmp += 1

                        numero_folio_final = concatenate_folio(folio_tmp, numero_folio, folio_nota)
                        try:
                            vale = ValeAlmacenGeneral.objects.get(no_folio=numero_folio_final)
                        except ValeAlmacenGeneral.DoesNotExist:                        
                            vale = ValeAlmacenGeneral.objects.create(
                                vale_llantas=False, # es almacen general
                                no_folio=numero_folio_final,
                                observaciones_grales='loaded_from_migration',
                                tipo_movimiento=tme,
                                fecha_vale = f_movimiento,
                                persona_asociada = obj_proveedor,
                                creador_vale=admin_profile,
                                con_iva=bandera_iva
                            )
                        vale_anterior = vale

                    else: # usa la ultima factura
                        vale_anterior


                    '''
                    if producto: # encuentra el producto
                        pass

                    '''



            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('Resumen'))                                              
            self.stdout.write(self.style.SUCCESS('Productos: .......... existen    :{}'.format(existe_producto)))    # 210 ..... 583
            self.stdout.write(self.style.SUCCESS('Productos ........... no existen :{}'.format(no_existe_producto))) # 672 ..... 299
            self.stdout.write(self.style.SUCCESS('Productos ........... repetidos  :{}'.format(repetidos)))          # 0
            self.stdout.write(self.style.SUCCESS('Todos ..........................  {}'.format(todos)))              # 882 ..... 882
