from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import Status
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load status from CSV.'
    def handle(self, *args, **options):
        
        with open(settings.BASE_DIR + '/almacen/load_init/status.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().capitalize()
                    #codigo = row[1].strip()
                    obj, bandera = Status.objects.get_or_create(nombre=nombre)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Status creada: {}'.format(obj.nombre)))
                    else:
                        self.stdout.write(self.style.ERROR('Status ya existia: {}'.format(obj.nombre)))