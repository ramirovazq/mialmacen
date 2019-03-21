from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import Marca
from django.utils import timezone
import csv, os

class Command(BaseCommand):
    help = 'Load marcas from CSV.'
    def handle(self, *args, **options):
        print(settings.BASE_DIR)
        with open(settings.BASE_DIR + '/load_init/marcas.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    nombre = row[0].strip().capitalize()
                    codigo = row[1].strip()
                    obj, bandera = Marca.objects.get_or_create(nombre=nombre, codigo=codigo)
                    if bandera:
                        self.stdout.write(self.style.SUCCESS('Marca creada: {} [{}]'.format(obj.nombre, obj.codigo)))
                    else:
                        self.stdout.write(self.style.ERROR('Marca ya existia: {} [{}]'.format(obj.nombre, obj.codigo)))