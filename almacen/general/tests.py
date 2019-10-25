from django.test import TestCase
from django.contrib.auth.models import User

from .models import *
from persona.models import Position, ProfilePosition
from llantas.utils import *

import datetime


class ProductosMovimientoTestCase(TestCase):

    def setUp(self):

        self.user01 = return_profile("rosa")
        self.user02 = return_profile("goyo")

        self.conteo = return_profile("CONTETO", "ABSTRACT")
        self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        self.bodega02 = return_profile("ALMACEN_ALTERNO", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")

        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida  = TipoMovimiento.objects.create(nombre="SALIDA")

        tipo_smaller,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="-1")
        tipo_reference, bandera = TipoUnidadMedida.objects.get_or_create(tipo="0")
        tipo_greater,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="1")

        categoria_longitud, bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Longitud/Distancia")
        categoria_unidad,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Unidad")

        self.fourfeb = datetime.datetime.strptime('04/02/2019', "%d/%m/%Y").date()

        self.metro = UnidadMedida.objects.create(
            nombre="metro",
            categoria=categoria_longitud,
            tipo_unidad=tipo_reference,
            ratio=1,
            simbolo="m"
            )

        self.centimetros = UnidadMedida.objects.create(
            nombre="centímetros",
            categoria=categoria_longitud,
            tipo_unidad=tipo_smaller,
            ratio=0.01,
            simbolo="cm"
            )

        self.kilometro = UnidadMedida.objects.create(
            nombre="kilometros",
            categoria=categoria_longitud,
            tipo_unidad=tipo_greater,
            ratio=1000,
            simbolo="km"
            )


        self.vale01 = ValeAlmacenGeneral.objects.create(
                no_folio="0001",
                observaciones_grales="nada",
                tipo_movimiento=self.tm_entrada,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )

        self.cable_cuatro = Producto.objects.create(nombre="Cable #4")

    def test_three_entries_one_warehouse(self):

        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )

        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )

        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )


        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory()
        self.assertEqual(float(quantity_cable_inventory), 3005.7) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference





    def test_entries_different_warehouses(self):
        # bodega002
        zero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=35, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )

        # bodega01
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )

        # bodega01
        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )
        # bodega01
        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )
        # bodega02
        cuarto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=18, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )

        # in total, for both warehouses
        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory()
        self.assertEqual(float(quantity_cable_inventory), 3058.7) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference

        # by each warehouse
        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory(self.bodega01)
        self.assertEqual(float(quantity_cable_inventory), 3005.7) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference

        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory(self.bodega02)
        self.assertEqual(float(quantity_cable_inventory), 53.0) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference





    def test_entries_with_outputs_different_warehouses(self):

        # entry bodega02
        zero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=35, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )


        # entry bodega01
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )

        # entry bodega01
        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )

        # entry bodega01
        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )

        # entry bodega02
        cuarto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=18, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )

        # output bodega02
        zero_mov_output = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento= self.tm_salida,
            fecha_movimiento=self.fourfeb,            

            origen=self.bodega02,
            destino=self.tractor01,


            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=13, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )


        # output bodega01
        zero_mov_output = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento= self.tm_salida,
            fecha_movimiento=self.fourfeb,            

            origen=self.bodega01,
            destino=self.tractor01,

            producto=self.cable_cuatro,
            unidad= self.centimetros,
            cantidad=60, # 60 cm
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )


        # in total, for both warehouses
        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory()
        self.assertEqual(float(quantity_cable_inventory), 3045.1) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference

        # by each warehouse
        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory(self.bodega01)
        self.assertEqual(float(quantity_cable_inventory), 3005.1) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference

        quantity_cable_inventory, cable_units = self.cable_cuatro.inventory(self.bodega02)
        self.assertEqual(float(quantity_cable_inventory), 40.0) # must be 5.7 m + 3 km
        self.assertEqual(cable_units, self.metro) # must be metro, its tipo reference



class ProductosMovimientoPositionTestCase(TestCase):

    def setUp(self):

        self.user01 = return_profile("rosa")
        self.user02 = return_profile("goyo")

        self.conteo = return_profile("CONTETO", "ABSTRACT")
        self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        self.bodega02 = return_profile("ALMACEN_ALTERNO", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")

        anaquel_one = Position.objects.create(name="Anaquel 1")
        nivel_one   = Position.objects.create(name="Nivel de Anaquel 1", parent=anaquel_one)
        nivel_six   = Position.objects.create(name="Nivel de Anaquel 6", parent=anaquel_one)

        self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)

        anaquel_eleven = Position.objects.create(name="Anaquel 11")
        nivel_twenty_three   = Position.objects.create(name="Nivel de Anaquel 23", parent=anaquel_eleven)
        nivel_twenty_four    = Position.objects.create(name="Nivel de Anaquel 24", parent=anaquel_eleven)

        self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)


        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida  = TipoMovimiento.objects.create(nombre="SALIDA")

        tipo_smaller,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="-1")
        tipo_reference, bandera = TipoUnidadMedida.objects.get_or_create(tipo="0")
        tipo_greater,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="1")

        categoria_longitud, bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Longitud/Distancia")
        categoria_unidad,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Unidad")

        self.fourfeb = datetime.datetime.strptime('04/02/2019', "%d/%m/%Y").date()

        self.metro = UnidadMedida.objects.create(
            nombre="metro",
            categoria=categoria_longitud,
            tipo_unidad=tipo_reference,
            ratio=1,
            simbolo="m"
            )

        self.centimetros = UnidadMedida.objects.create(
            nombre="centímetros",
            categoria=categoria_longitud,
            tipo_unidad=tipo_smaller,
            ratio=0.01,
            simbolo="cm"
            )

        self.kilometro = UnidadMedida.objects.create(
            nombre="kilometros",
            categoria=categoria_longitud,
            tipo_unidad=tipo_greater,
            ratio=1000,
            simbolo="km"
            )


        self.vale01 = ValeAlmacenGeneral.objects.create(
                no_folio="0001",
                observaciones_grales="nada",
                tipo_movimiento=self.tm_entrada,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )

        self.cable_cuatro = Producto.objects.create(nombre="Cable #4")




    def test_three_entries_one_warehouse(self):

        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )

        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=primer_mov_entrada
        )

        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )

        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=segundo_mov_entrada
        )

        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )

        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_six,
            movimiento=tercer_mov_entrada
        )

        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)

        exactposition_cable_cuatro = self.cable_cuatro.positions()
        uno = self.bodega01_nivel_one in exactposition_cable_cuatro
        dos = self.bodega01_nivel_six in exactposition_cable_cuatro

        self.assertEqual(uno, True)
        self.assertEqual(dos, True)
        self.assertEqual(len(exactposition_cable_cuatro), 2)




    def test_entries_different_warehouses(self):
        # bodega002
        zero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=35, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega02_nivel_twenty_three,
            movimiento=zero_mov_entrada
        )
        #self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        #self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)
        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)


        # bodega01
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=primer_mov_entrada
        )
        #self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        #self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)
        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)


        # bodega01
        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=segundo_mov_entrada
        )
        #self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        #self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)
        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)


        # bodega01
        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_six,
            movimiento=tercer_mov_entrada
        )
        #self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        #self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)
        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)


        # bodega02
        cuarto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=18, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega02_nivel_twenty_four,
            movimiento=cuarto_mov_entrada
        )
        #self.bodega02_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_three)
        #self.bodega02_nivel_twenty_four = ProfilePosition.objects.create(profile=self.bodega02, position=nivel_twenty_four)
        #self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        #self.bodega01_nivel_six = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_six)


        exactposition_cable_cuatro = self.cable_cuatro.positions()
        uno    = self.bodega01_nivel_one in exactposition_cable_cuatro
        dos    = self.bodega01_nivel_six in exactposition_cable_cuatro
        tres   = self.bodega02_nivel_twenty_three in exactposition_cable_cuatro
        cuatro = self.bodega02_nivel_twenty_four in exactposition_cable_cuatro

        self.assertEqual(uno, True)
        self.assertEqual(dos, True)
        self.assertEqual(tres, True)
        self.assertEqual(cuatro, True)
        self.assertEqual(len(exactposition_cable_cuatro), 4)


        exactposition_cable_cuatro = self.cable_cuatro.positions(self.bodega01)
        uno    = self.bodega01_nivel_one in exactposition_cable_cuatro
        dos    = self.bodega01_nivel_six in exactposition_cable_cuatro
        self.assertEqual(len(exactposition_cable_cuatro), 2)


        exactposition_cable_cuatro = self.cable_cuatro.positions(self.bodega02)
        tres   = self.bodega02_nivel_twenty_three in exactposition_cable_cuatro
        cuatro = self.bodega02_nivel_twenty_four in exactposition_cable_cuatro
        self.assertEqual(len(exactposition_cable_cuatro), 2)



    def test_entries_different_warehouses_exact_quantity(self):
        # bodega002
        zero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=35, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega02_nivel_twenty_three,
            movimiento=zero_mov_entrada
        )

        # bodega01
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=5, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=primer_mov_entrada
        )

        # bodega01
        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.centimetros,
            cantidad=70, # s metros
            precio_unitario=15,
            creador=self.user01,
            observacion="2do movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=segundo_mov_entrada
        )

        # bodega01
        tercer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.kilometro,
            cantidad=3, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_six,
            movimiento=tercer_mov_entrada
        )

        # bodega02
        cuarto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega02,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=18, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="3er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega02_nivel_twenty_four,
            movimiento=cuarto_mov_entrada
        )


        exactposition_cable_cuatro_inventory = self.cable_cuatro.positions_inventory()
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 23"], 35)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1"], 5.7)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 6"], 3000)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 24"], 18)
'''
        self.bodega02_nivel_twenty_three   35 m       "ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 23": 35
        self.bodega01_nivel_one            5m  + .7    "ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1": 5.7
        self.bodega01_nivel_six            3000 m      "ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 6": 3000
        self.bodega02_nivel_twenty_four    18 m        "ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 24": 18
'''
