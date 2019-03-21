from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import Medida
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load medidas from CSV.'
    def handle(self, *args, **options):        
        with open(settings.BASE_DIR + '/load_init/medidas.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().upper()
                    codigo = Medida.siguiente_codigo()
                    obj, bandera = Medida.objects.get_or_create(nombre=nombre, defaults={'codigo': codigo})
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Medida creada: {} [{}]'.format(obj.nombre, obj.codigo)))
                    else:
                        self.stdout.write(self.style.ERROR('Medida ya existia: {} [{}]'.format(obj.nombre, obj.codigo)))