from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone

from llantas.utils import *
from llantas.models import *
from general.models import *
from persona.models import *

import csv, os, datetime

class Command(BaseCommand):
    help = 'Migrate numero de parte, to more flexible model.'


    def handle(self, *args, **options):
        
        def cure_string(cadena):
            cadena = cadena.strip() # quita espacios adelante y atras
            lista_cadena = cadena.split(",")
            return lista_cadena


        for producto in Producto.objects.all():
            lista_total = []
            lista_numero_de_parte_uno = []
            lista_numero_de_parte_dos = []
            if producto.numero_de_parte_uno:
                lista_numero_de_parte_uno = cure_string(producto.numero_de_parte_uno)
            if producto.numero_de_parte_dos:
                lista_numero_de_parte_dos = cure_string(producto.numero_de_parte_dos)

            # here, migrate to new table NumeroParte
            if producto.numero_de_parte_uno or producto.numero_de_parte_dos:
                lista_total = lista_numero_de_parte_uno + lista_numero_de_parte_dos
                for x in lista_total:
                    try:
                        n = NumeroParte.objects.get(producto=producto, numero_de_parte=x)
                        self.stdout.write(self.style.ERROR("ya existia {} con numero de parte {} ".format(n.producto, n.numero_de_parte)))
                    except NumeroParte.DoesNotExist:
                        n = NumeroParte.objects.create(producto=producto, numero_de_parte=x)
                        self.stdout.write(self.style.SUCCESS("se genera {} con numero de parte {} ".format(n.producto, n.numero_de_parte)))

                # here we clean, cause already migrated
                producto.numero_de_parte_uno = None
                producto.numero_de_parte_dos = None
                producto.save()
            else:
                self.stdout.write(self.style.ERROR("no existen numeros de parte en antigua tabla "))

