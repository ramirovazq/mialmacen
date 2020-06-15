from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from llantas.models import Marca
from django.utils import timezone
import csv, os

'''
This command verify if one Marca Doesnt exist in the database. If doesnt exist, then prints wich needs to be added.
'''
class Command(BaseCommand):
    help = 'Load marcas from CSV.'
    def handle(self, *args, **options):
        with open(settings.BASE_DIR + '/load_init/all_marcas_unique.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            for indice, row in enumerate(readCSV):
                nombre = row[0].strip().capitalize()                    
                codigo = Marca.siguiente_codigo()
                try:
                    Marca.objects.get(nombre=nombre)
                    #print("{}".format(nombre))
                except Marca.DoesNotExist:
                    print("NO...;{}".format(nombre))
                '''
                obj, bandera = Marca.objects.get_or_create(nombre=nombre, defaults={'codigo': codigo})
                if bandera:
                    self.stdout.write(self.style.SUCCESS('Marca creada: {} [{}]'.format(obj.nombre, obj.codigo)))
                else:
                    self.stdout.write(self.style.ERROR('Marca ya existia: {} [{}]'.format(obj.nombre, obj.codigo)))
                '''
'''
# all marca names capitalize
for x in Marca.objects.all():
   correcto = "{}".format(x.nombre.strip().capitalize())
   x.nombre = correcto
   x.save()
'''