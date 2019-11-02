from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from llantas.utils import *
from llantas.models import *
from general.models import *
from persona.models import *

import csv, os, datetime

class Command(BaseCommand):
    help = 'Load init movimientos from CSV, for almacen general.'
    def handle(self, *args, **options):
        
        pa = return_profile('rvazquez')# valor fijo

        with open(settings.BASE_DIR + '/load_init/fletes_almacen_general.csv') as csvfile_in:
            readCSV = csv.reader(csvfile_in, delimiter=';')

            tipo_smaller,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="-1")
            tipo_reference, bandera = TipoUnidadMedida.objects.get_or_create(tipo="0")
            tipo_greater,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="1")

            categoria_longitud, bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Longitud/Distancia") # metros, cm
            categoria_unidad,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Unidad")
            categoria_peso,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Peso") #kg
            categoria_volumen,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Volumen") #lts

            centimetro, band = UnidadMedida.objects.get_or_create(
                nombre="Centímetro",
                categoria=categoria_longitud,
                tipo_unidad=tipo_smaller,
                ratio=.01,
                simbolo="m"
            )

            metro, band = UnidadMedida.objects.get_or_create(
                nombre="Metro",
                categoria=categoria_longitud,
                tipo_unidad=tipo_reference,
                ratio=1,
                simbolo="m"
            )

            litro, band = UnidadMedida.objects.get_or_create(
                nombre="Litro",
                categoria=categoria_volumen,
                tipo_unidad=tipo_reference,
                ratio=1,
                simbolo="L"
            )

            kilogramo, band = UnidadMedida.objects.get_or_create(
                nombre="Kilogramo",
                categoria=categoria_volumen,
                tipo_unidad=tipo_reference,
                ratio=1,
                simbolo="kg"
            )

            unidad_gral, band = UnidadMedida.objects.get_or_create(
                nombre="Unidad",
                categoria=categoria_unidad,
                tipo_unidad=tipo_reference,
                ratio=1,
                simbolo="u"
            )

            dicc_unidades = {
                "-": unidad_gral,
                "MTS": metro ,
                "LTS": litro,
                "KGS": kilogramo,
                "KG": kilogramo,
                "COM": centimetro,
                "CM": centimetro,
            }


            for indice, row in enumerate(readCSV):
                if indice == 0:
                    bodega_title           = row[0].strip().upper() # ENTRADA SALIDA ## mayusculas
                    print(row[1])
                    anaquel_title          = row[1].strip().upper() # ENTRADA SALIDA ## mayusculas
                    nivel_anaquel_title    = row[2].strip().upper() # ENTRADA SALIDA ## mayusculas
                    producto_title         = row[3].strip() # ENTRADA SALIDA ## mayusculas
                    cantidad_title         = row[4].strip() # ENTRADA SALIDA ## mayusculas
                    unidad_title           = row[5].strip() # ENTRADA SALIDA ## mayusculas
                    tipo_movimiento_title  = row[6].strip() # ENTRADA SALIDA ## mayusculas
                    fecha_movimiento_title = row[7].strip() # ENTRADA SALIDA ## mayusculas
                    no_folio_title         = row[8].strip() # ENTRADA SALIDA ## mayusculas
                    origen_title           = row[9].strip() # ENTRADA SALIDA ## mayusculas
                    precio_unitario_title  = row[10].strip() # ENTRADA SALIDA ## mayusculas
                else: # quit name of column
                    destino                = row[0].strip().upper() # ENTRADA SALIDA ## mayusculas
                    anaquel                = "{} {}".format(anaquel_title, row[1].strip().upper()) # ENTRADA SALIDA ## mayusculas
                    nivel_anaquel          = "{} {}".format(nivel_anaquel_title, row[2].strip().upper()) # ENTRADA SALIDA ## mayusculas
                    producto_original      = row[3].strip() # ENTRADA SALIDA ## mayusculas
                    producto_original      = producto_original.upper() # ENTRADA SALIDA ## mayusculas
                    cantidad               = row[4].strip() # ENTRADA SALIDA ## mayusculas
                    unidad_                 = row[5].strip() # ENTRADA SALIDA ## mayusculas
                    if unidad_:
                        unidad                 = unidad_.upper() # ENTRADA SALIDA ## mayusculas
                    else:
                        unidad = "-"
                    tipo_movimiento        = row[6].strip().upper()
                    f_movimiento           = row[7].strip()
                    fecha_movimiento       = datetime.datetime.strptime(f_movimiento, "%d/%m/%y").date()
                    no_folio               = row[8].strip()
                    origen                 = row[9].strip() # ENTRADA SALIDA ## mayusculas
                    precio_unitario        = row[10].strip() # ENTRADA SALIDA ## mayusculas

                    if not precio_unitario:
                        precio_unitario = 0.0

                    if destino: 
                        destino_obj = return_profile(destino, "BODEGA")
                    ## valores del Vale
                    if origen:
                        origen_obj  = return_profile(origen, "BODEGA")
                    admin_profile   = return_profile("admin", "STAFF")
                    
                    if anaquel:
                        anaquel_obj, anaquel_flag         = Position.objects.get_or_create(name=anaquel)                        
                    if nivel_anaquel:
                        nivel_anaquel_obj, n_anaquel_flag = Position.objects.get_or_create(name=nivel_anaquel, parent=anaquel_obj)

                    if anaquel and nivel_anaquel: # si ambos existen                        
                        profileposition_obj, profileposition_bandera = ProfilePosition.objects.get_or_create(profile=destino_obj, position=nivel_anaquel_obj)
                    elif anaquel and not nivel_anaquel:
                        profileposition_obj, profileposition_bandera = ProfilePosition.objects.get_or_create(profile=destino_obj, position=anaquel_obj)


                    #no_folio = "XXXX"                    
                    fecha_vale = datetime.datetime.strptime(f_movimiento, "%d/%m/%y").date()                    
                    tme, tme_flag = TipoMovimiento.objects.get_or_create(nombre=tipo_movimiento)

                    vale_inicial, vale_inicial_flag = ValeAlmacenGeneral.objects.get_or_create(
                        no_folio=no_folio, 
                        tipo_movimiento=tme,
                        fecha_vale=fecha_vale,
                        persona_asociada=admin_profile, ## el proveedor o quien_entrega el vale
                        creador_vale=admin_profile,
                        defaults={"observaciones_grales":"Carga inicial de el inventario general."})

                    if vale_inicial_flag:
                        self.stdout.write(self.style.SUCCESS('Se genero el vale #{}'.format(no_folio)))
                    else:
                        self.stdout.write(self.style.ERROR('Ya estaba generado el vale #{}'.format(no_folio)))



                    # Lllanta
                    producto, p_flag = Producto.objects.get_or_create(nombre=producto_original)

                    if p_flag:
                        self.stdout.write(self.style.SUCCESS('Se genero el producto #{}'.format(producto)))
                    else:
                        self.stdout.write(self.style.ERROR('Ya estaba generado el producto #{}'.format(producto)))

                    try:
                        dicc_mov_default = {
                            "precio_unitario":precio_unitario,
                            "origen":origen_obj,
                            "destino":destino_obj,
                            "unidad":dicc_unidades[unidad],
                            "cantidad":cantidad
                        }

                        movimiento, bandera_movimiento = MovimientoGeneral.objects.get_or_create(
                            vale=vale_inicial,
                            tipo_movimiento=vale_inicial.tipo_movimiento,
                            fecha_movimiento = vale_inicial.fecha_vale,                         
                            creador=vale_inicial.persona_asociada,
                            producto=producto,
                            observacion="",
                            defaults=dicc_mov_default
                        )
                        #movimiento.save()


                        a, b = ProductoExactProfilePosition.objects.get_or_create(
                            exactposition=profileposition_obj,
                            movimiento=movimiento
                        )


                        if bandera_movimiento:
                            self.stdout.write(self.style.SUCCESS('Movimiento creado {}'.format(movimiento.id)))
                        else:
                            self.stdout.write(self.style.ERROR('Movimiento NO creado ********************************************************** ya existia'))
                    except KeyError:
                        self.stdout.write(self.style.ERROR('ERROR EN UNIDAD ... ***************************************************************'))