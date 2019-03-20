from django.core.management.base import BaseCommand, CommandError
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

        with open(settings.BASE_DIR + '/almacen/load_init/movimientos.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column

                    tipo_movimiento  = row[0].strip().upper() # ENTRADA SALIDA ## mayusculas
                    f_movimiento = row[1].strip()
                    fecha_movimiento = datetime.datetime.strptime(f_movimiento, "%d/%m/%Y").date()
                    no_folio         = row[2].strip()

                    origen           = row[3].strip()
                    destino          = row[4].strip()
                    
                    ## GENERAL LA LLANTA
                    marca            = row[6].strip().capitalize() # Solo primera letra mayuscula
                    medida           = row[7].strip().upper() ## mayusculas
                    posicion         = row[8].strip().upper() ## mayusculas
                    status           = row[10].strip().capitalize() # Solo primera letra mayuscula
                    dot              = row[11].strip() ## es numerico

                    cantidad         = row[9].strip()
                    precio_unitario  = row[12]
                    if not precio_unitario:
                        precio_unitario = 0.0


                    ## valores del Vale
                    
                    #no_folio = "XXXX"                    
                    fecha_vale = datetime.datetime.strptime(f_movimiento, "%d/%m/%Y").date()                    
                    tme, tme_flag = TipoMovimiento.objects.get_or_create(nombre=tipo_movimiento)

                    vale_inicial, vale_inicial_flag = Vale.objects.get_or_create(
                        no_folio=no_folio, 
                        tipo_movimiento=tme,
                        fecha_vale=fecha_vale,
                        persona_asociada=pa,
                        creador_vale=pa,
                        defaults={"observaciones_grales":"Carga inicial de el inventario."})

                    if vale_inicial_flag:
                        self.stdout.write(self.style.SUCCESS('Se genero el vale #{}'.format(no_folio)))
                    else:
                        self.stdout.write(self.style.ERROR('Ya estaba generado el vale #{}'.format(no_folio)))


                    profile_origen = return_profile(origen, "ABSTRACT")
                    profile_destino = return_profile(destino, "BODEGA")

                    # Lllanta
                    m, m_flag = Marca.objects.get_or_create(nombre=marca)
                    me, me_flag = Medida.objects.get_or_create(nombre=medida)
                    pos, pos_flag = Posicion.objects.get_or_create(nombre=posicion)
                    sta, sta_flag = Status.objects.get_or_create(nombre=status)
                    # dot

                    llanta, llanta_flag = Llanta.objects.get_or_create(
                        marca=m,
                        medida=me,
                        posicion=pos,
                        status=sta,
                        dot=dot
                    )

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