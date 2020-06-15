from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from llantas.utils import *
from llantas.models import *
from persona.models import Profile

import csv, os, datetime

class Command(BaseCommand):
    help = 'Load init movimientos from CSV.'
    def handle(self, *args, **options):
        
        pa = return_profile('rvazquez')# valor fijo

        with open(settings.BASE_DIR + '/load_init/inventario_actualizado_loading.csv') as csvfile_in:
            index_count = 0
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                index_count += 1
                if indice != 0: # quit name of column
                    print("indice {} -- ROW .... {}".format(index_count, row))

                    tipo_movimiento  = row[0].strip().upper() # ENTRADA SALIDA ## mayusculas
                    f_movimiento = row[1].strip()
                    fecha_movimiento = datetime.datetime.strptime(f_movimiento, "%d/%m/%Y").date()
                    no_folio         = row[2].strip()

                    origen           = row[3].strip()
                    destino          = row[4].strip()
                    
                    ## GENERAL LA LLANTA
                    marca            = row[6].strip().capitalize() # Solo primera letra mayuscula
                    vida             = row[7].strip()# es un entero

                    medida           = row[8].strip().upper() ## mayusculas
                    posicion         = row[9].strip().upper() ## mayusculas  Direccion o traccion
                    cantidad         = row[10].strip()

                    status           = row[11].strip().capitalize() # Solo primera letra mayuscula
                    dot              = row[12].strip() ## es numerico

                    if "(" in dot: # rows with 
                        dot_observacion = dot 
                        lista_dot = dot.split("(") # ['4519', '4619)']
                        dot = lista_dot[0]
                    else:
                        dot_observacion = ""
                    
                    precio_unitario  = row[13]
                    if not precio_unitario:
                        precio_unitario = 0.0

                    permisionario    = row[14]
                    if permisionario: 
                        permisionario = row[14].strip().upper() # permisionario
                        permisionario_obj = return_profile(permisionario, "PERMISIONARIO")

                    ## valores del Vale
                    if origen == "CONTEO_12JUNIO":
                        profile_origen = return_profile(origen, "ABSTRACT")
                    else:
                        profile_origen = return_profile(origen, "BODEGA")

                    if destino == "BODEGA_GENERAL":
                        profile_destino = return_profile(destino, "BODEGA")
                    else:
                        profile_destino = return_profile(destino, "ECONOMICO")
                    
                    #no_folio = "XXXX"                    
                    fecha_vale = datetime.datetime.strptime(f_movimiento, "%d/%m/%Y").date()                    
                    tme, tme_flag = TipoMovimiento.objects.get_or_create(nombre=tipo_movimiento)

                    vale_inicial, vale_inicial_flag = Vale.objects.get_or_create(
                        no_folio=no_folio, 
                        tipo_movimiento=tme,
                        fecha_vale=fecha_vale,
                        persona_asociada=profile_origen, ## el proveedor o quien_entrega el vale
                        creador_vale=pa,
                        defaults={"observaciones_grales":"Carga inicial de el inventario."})

                    if vale_inicial_flag:
                        self.stdout.write(self.style.SUCCESS('Se genero el vale #{}'.format(no_folio)))
                    else:
                        self.stdout.write(self.style.ERROR('Ya estaba generado el vale #{}'.format(no_folio)))



                    # Lllanta
                    m, m_flag = Marca.objects.get_or_create(nombre=marca)
                    me, me_flag = Medida.objects.get_or_create(nombre=medida)
                    pos, pos_flag = Posicion.objects.get_or_create(nombre=posicion)
                    sta, sta_flag = Status.objects.get_or_create(nombre=status)
                    # dot

                    if vida:
                        llanta, llanta_flag = Llanta.objects.get_or_create(
                            marca=m,
                            medida=me,
                            posicion=pos,
                            status=sta,
                            dot=dot,
                            porciento_vida=vida
                        )
                    else:
                        # default 100 por ciento
                        try:
                            llanta, llanta_flag = Llanta.objects.get_or_create(
                                marca=m,
                                medida=me,
                                posicion=pos,
                                status=sta,
                                dot=dot
                            )
                        except MultipleObjectsReturned:
                            llanta = Llanta.objects.filter(marca=m, 
                                    medida=me, 
                                    posicion=pos,
                                    status=sta,
                                    dot=dot,
                                    porciento_vida=100).first()

                    if permisionario:
                        movimiento = Movimiento(
                            vale=vale_inicial,
                            tipo_movimiento=vale_inicial.tipo_movimiento,
                            fecha_movimiento = vale_inicial.fecha_vale, 
                            origen=profile_origen,
                            destino=profile_destino,
                            llanta=llanta,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            creador=vale_inicial.persona_asociada, 
                            permisionario=permisionario_obj,
                            observacion=dot_observacion
                        )
                    else:
                        movimiento = Movimiento(
                        vale=vale_inicial,
                        tipo_movimiento=vale_inicial.tipo_movimiento,
                        fecha_movimiento = vale_inicial.fecha_vale, 
                        origen=profile_origen,
                        destino=profile_destino,
                        llanta=llanta,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        creador=vale_inicial.persona_asociada, 
                        observacion=dot_observacion
                    )
                    movimiento.save()
                    if movimiento.id:
                        self.stdout.write(self.style.SUCCESS('Movimiento creado {}'.format(movimiento.id)))
                    else:
                        self.stdout.write(self.style.ERROR('Movimiento NO creado'))
                    '''
                    obj, bandera = Marca.objects.get_or_create(nombre=nombre, codigo=codigo)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Marca creada: {} [{}]'.format(obj.nombre, obj.codigo)))
                    else:
                        self.stdout.write(self.style.ERROR('Marca ya existia: {} [{}]'.format(obj.nombre, obj.codigo)))
                    '''