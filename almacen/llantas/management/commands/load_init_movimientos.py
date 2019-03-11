from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from llantas.models import *
from persona.models import Profile

import csv, os, datetime

class Command(BaseCommand):
    help = 'Load init movimientos from CSV.'
    def handle(self, *args, **options):
        
        def return_user(username):
            try:
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                u = User.objects.create_user(username, '{}@fletesexpress.com.mx'.format(username), 'esteesunpasswordtest785412')
            return u

        with open(settings.BASE_DIR + '/almacen/load_init/movimientos.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    tipo_movimiento  = row[0].strip()
                    f_movimiento = row[1].strip()
                    fecha_movimiento = datetime.datetime.strptime(f_movimiento, "%d/%m/%Y").date()
                    no_folio         = row[2].strip()

                    origen           = row[3].strip()
                    destino          = row[4].strip()
                                      ## SKU
                    marca            = row[6].strip().capitalize()
                    medida           = row[7].strip().upper()
                    posicion         = row[8].strip().upper()
                    cantidad         = row[9].strip()
                    status           = row[10].strip().capitalize()
                    dot              = row[11].strip()
                    precio_unitario  = row[12]
                    if not precio_unitario:
                        precio_unitario = 0.0


                    usuario_origen = return_user(origen)
                    usuario_destino = return_user(destino)
                    tm, tm_flag = TipoMovimiento.objects.get_or_create(nombre=tipo_movimiento)
                    po , po_flag = Profile.objects.get_or_create(user=usuario_origen)
                    pd, pd_flag = Profile.objects.get_or_create(user=usuario_destino)
                    m, m_flag = Marca.objects.get_or_create(nombre=marca)
                    me, me_flag = Medida.objects.get_or_create(nombre=medida)
                    pos, pos_flag = Posicion.objects.get_or_create(nombre=posicion)
                    sta, sta_flag = Status.objects.get_or_create(nombre=status)

                    movimiento = Movimiento(
                        tipo_movimiento = tm,
                        fecha_movimiento =fecha_movimiento, 
                        no_folio=no_folio,
                        origen=po,
                        destino=pd,
                        marca=m,
                        medida=me,
                        posicion=pos,
                        cantidad=cantidad,
                        status=sta,
                        dot=dot,
                        precio_unitario=precio_unitario
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