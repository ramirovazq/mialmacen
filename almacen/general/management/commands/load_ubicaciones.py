from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.utils import timezone

from persona.models import Position, Tipo, Profile, ProfilePosition
from llantas.utils import return_profile
import csv, os, datetime

class Command(BaseCommand):
    help = 'Load ubicaciones from CSV, to almacen general.'
    def handle(self, *args, **options):
        '''
        lee el archivo ubicaciones.csv
        Posición	PosiciónDescripción
        BA1N1	BODEGA_GENERAL>>ANAQUEL 1>>NIVEL DE ANAQUEL 1
        '''

        with open(settings.BASE_DIR + '/load_init/ubicaciones.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')
            profile_no_existente = 0
            profile_existente = 0
            for indice, row in enumerate(readCSV):
                if indice != 0: # quit name of column
                    position_string =  row[1]
                    list_positions = position_string.split(">>")
                    if len(list_positions) > 0:
                        # code for profile
                        tipo_ = "BODEGA"
                        tipo = Tipo.objects.get(nombre=tipo_)
                        profile_username = list_positions.pop(0)
                        profile_username = profile_username.strip().upper()
                        try:
                            u = User.objects.get(username=profile_username)
                            p = Profile.objects.get(user=u)
                            existe_usuario = True
                            existe_profile = True
                        except Profile.DoesNotExist:
                            existe_profile = False
                        except User.DoesNotExist:
                            existe_usuario = False

                        if not(existe_usuario) or not(existe_profile):
                            p = return_profile(profile_username)
                            print("new_profile: {}".format(p))
                            profile_no_existente += 1
                        else:
                            profile_existente += 1
                            print("profile: {}".format(p))

                        # list of positions
                        # make sure exist all positions
                        for position_name in list_positions:
                                positions = Position.objects.filter(name=position_name)
                                if len(positions) == 0:
                                    position = Position.objects.create(name=position_name)
                                elif len(positions) == 1:
                                    position = positions[0]
                                else:
                                    print("MANY... position {}".format(position_name))
                                    position = positions[0]                    
                        parent = None
                        for position_name in list_positions:
                            if parent:
                                parent, bandera = Position.objects.get_or_create(name=position_name, parent=parent)
                                continue
                            parent = Position.objects.get(name=position_name)
                        # P   
                        # A >> B >> C >> D
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<")
                        print(parent)

                        print("last step >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        pp, band_pp = ProfilePosition.objects.get_or_create(profile=p, position=parent)
                        print(pp)
                        
                    