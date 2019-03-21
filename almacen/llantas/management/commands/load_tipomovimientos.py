from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import TipoMovimiento
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load tipo de movimientos from CSV. ENTRADA SALIDA'
    def handle(self, *args, **options):
        
        with open(settings.BASE_DIR + '/load_init/tipodemovimientos.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().upper()
                    #codigo = row[1].strip()
                    obj, bandera = TipoMovimiento.objects.get_or_create(nombre=nombre)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('TipoMovimiento creada: {}'.format(obj.nombre)))
                    else:
                        self.stdout.write(self.style.ERROR('TipoMovimiento ya existia: {}'.format(obj.nombre)))