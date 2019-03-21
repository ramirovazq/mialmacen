from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from persona.models import Tipo
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load tipo de profiles from CSV.'
    def handle(self, *args, **options):
        
        with open(settings.BASE_DIR + '/load_init/tipodeprofiles.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().upper()
                    obj, bandera = Tipo.objects.get_or_create(nombre=nombre)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Tipo creada: {}'.format(obj.nombre)))
                    else:
                        self.stdout.write(self.style.ERROR('Tipo ya existia: {}'.format(obj.nombre)))