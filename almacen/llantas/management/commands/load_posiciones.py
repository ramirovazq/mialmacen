from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import Posicion
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load medidas from CSV.'
    def handle(self, *args, **options):
        
        with open(settings.BASE_DIR + '/almacen/load_init/posiciones.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().capitalize()
                    codigo = row[1].strip()
                    obj, bandera = Posicion.objects.get_or_create(nombre=nombre, codigo=codigo)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Posicion creada: {} [{}]'.format(obj.nombre, obj.codigo)))
                    else:
                        self.stdout.write(self.style.ERROR('Posicion ya existia: {} [{}]'.format(obj.nombre, obj.codigo)))