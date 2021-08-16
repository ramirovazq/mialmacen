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

        self.cable_cuatro.maximum = 5
        self.cable_cuatro.minimum = 1

    def test_minimum_less_than_limit(self):
        self.assertEqual(self.cable_cuatro.alarm_minimum(), True) 
        # 0 inventario actual -- minimo 1 y maximo 5 aunque está en el limito no hay alarma

    def test_minimum_equal_limit(self):
        MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=1, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        self.assertEqual(self.cable_cuatro.alarm_minimum(), True) 
        # 1 inventario actual -- minimo 1 y maximo 5 aunque está en el limito no hay alarma

    def test_minimum_mayor_than_limit(self):
        MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=2, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        self.assertEqual(self.cable_cuatro.alarm_minimum(), False) 
        # 1 inventario actual -- minimo 1 y maximo 5 aunque está en el limito no hay alarma



    def test_maximum_at_limit_not_alarm(self):

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
        self.assertEqual(self.cable_cuatro.alarm_maximum_and_minimum(), False) 
        # 5 inventario actual -- minimo 1 y maximo 5 aunque está en el limito no hay alarma

    def test_maximum_beyond_limit_alarm(self):

        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=7, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        self.assertEqual(self.cable_cuatro.alarm_maximum_and_minimum(), True) 
        # 7 inventario actual -- minimo 1 y maximo 5 aunque está en el limito no hay alarma

    def test_minimum_exact_limit_alarm(self):
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=1, # s metros
            precio_unitario=120.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        self.assertEqual(self.cable_cuatro.alarm_maximum_and_minimum(), True) 
        # 1 inventario actual -- minimo 1 y maximo 5 aunque está en el limite no hay alarma

    def test_minimum_with_zero(self):
        self.assertEqual(self.cable_cuatro.alarm_maximum_and_minimum(), True) 
        # 0 inventario actual -- minimo 1 y maximo 5 si hay alarma
        self.assertEqual(self.cable_cuatro.alarm_maximum_and_minimum(), True) 



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


        # bodega02
        quinto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento= self.tm_salida,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega02,            
            destino=self.tractor01,            
            producto=self.cable_cuatro,
            unidad=self.metro,
            cantidad=6, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="quinto movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega02_nivel_twenty_four,
            movimiento=quinto_mov_entrada
        )


        # bodega01
        sexto_mov_salida = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento= self.tm_salida,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega02,            
            destino=self.tractor01,            
            producto=self.cable_cuatro,
            unidad= self.kilometro ,
            cantidad=2, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="sexto movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_six,
            movimiento=sexto_mov_salida
        )

        # bodega01
        septimo_mov_salida = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento= self.tm_salida,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega02,            
            destino=self.tractor01,            
            producto=self.cable_cuatro,
            unidad= self.metro ,
            cantidad=377, # 3 kilometro
            precio_unitario=2000,
            creador=self.user01,
            observacion="septimo movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_six,
            movimiento=septimo_mov_salida
        )


        exactposition_cable_cuatro_inventory = self.cable_cuatro.positions_inventory()
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 23"], 35)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1"], 5.7)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 6"], 623.0)
        self.assertEqual(exactposition_cable_cuatro_inventory["ALMACEN_ALTERNO>>Anaquel 11>>Nivel de Anaquel 24"], 12.0)




class ProductosExactPositionTestCase(TestCase):

    def setUp(self):

        self.user01 = return_profile("rosa")
        self.user02 = return_profile("goyo")

        self.conteo = return_profile("CONTEO", "ABSTRACT")
        self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")

        anaquel_one = Position.objects.create(name="Anaquel 1")

        nivel_one            = Position.objects.create(name="Nivel de Anaquel 1", parent=anaquel_one)
        nivel_twenty_three   = Position.objects.create(name="Nivel de Anaquel 23", parent=anaquel_one)

        self.bodega01_nivel_one = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_one)
        self.bodega01_nivel_twenty_three = ProfilePosition.objects.create(profile=self.bodega01, position=nivel_twenty_three)

        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida  = TipoMovimiento.objects.create(nombre="SALIDA")

        tipo_smaller,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="-1")
        tipo_reference, bandera = TipoUnidadMedida.objects.get_or_create(tipo="0")
        tipo_greater,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="1")

        categoria_longitud, bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Longitud/Distancia")
        categoria_unidad,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Unidad")

        self.fourfeb = datetime.datetime.strptime('04/02/2019', "%d/%m/%Y").date()

        self.unidad = UnidadMedida.objects.create(
            nombre="unidad",
            categoria=categoria_unidad,
            tipo_unidad=tipo_reference,
            ratio=1,
            simbolo="m"
            )

        self.vale01 = ValeAlmacenGeneral.objects.create(
                no_folio="0001",
                observaciones_grales="nada",
                tipo_movimiento=self.tm_entrada,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )

        self.filtro_aire = Producto.objects.create(nombre="Filtros de aire")
        self.producto_x = Producto.objects.create(nombre="Producto X")

        self.vale02 = ValeAlmacenGeneral.objects.create(
                no_folio="0002",
                observaciones_grales="segunda entrada",
                tipo_movimiento=self.tm_entrada,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )

        self.vale03 = ValeAlmacenGeneral.objects.create(
                no_folio="0003",
                observaciones_grales="el 3ero de entrada",
                tipo_movimiento=self.tm_entrada,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )


        self.vale04 = ValeAlmacenGeneral.objects.create(
                no_folio="0004",
                observaciones_grales="el de salida",
                tipo_movimiento=self.tm_salida,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )

        self.vale05 = ValeAlmacenGeneral.objects.create(
                no_folio="0005",
                observaciones_grales="el de salida",
                tipo_movimiento=self.tm_salida,
                fecha_vale=self.fourfeb,
                persona_asociada=self.user02, # quien entrega
                creador_vale=self.user01,
            )



    def test_specific_locations_for_a_product(self):

        #vale01 # bodega01 # ENTRADA # nivel one #filtro_aire  12 
        other_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.vale01.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.producto_x,
            unidad=self.unidad,
            cantidad=500, 
            precio_unitario=150.5,
            creador=self.user01,
            observacion="otro movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=other_mov_entrada
        )


        #vale01 # bodega01 # ENTRADA # nivel one #filtro_aire  12 
        zero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.vale01.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=12, 
            precio_unitario=150.5,
            creador=self.user01,
            observacion="1er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=zero_mov_entrada
        )

        #vale01 # bodega01 # ENTRADA # nivel_one #filtro_aire 8  ( 12 + 8 )
        primer_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.vale01.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=8, # s metros
            precio_unitario=135.5,
            creador=self.user01,
            observacion="2do movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=primer_mov_entrada
        )


        #vale02 # bodega01 # ENTRADA # nivel_one #filtro_aire  15 ( 12 + 8 + 15 )
        segundo_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.vale02.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=15, # s metros
            precio_unitario=10.5,
            creador=self.user01,
            observacion="er movimiento"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=segundo_mov_entrada
        )


        #vale03 # bodega01 # ENTRADA # nivel_one #filtro_aire  100  (12 + 8 + 15 + 100 = 135 )
        tercero_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.vale03.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=100, # 
            precio_unitario=10.5,
            creador=self.user01,
            observacion="entrada 3er vale"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one,
            movimiento=tercero_mov_entrada
        )

        #vale03 # bodega01 # ENTRADA # nivel_twenty_three #filtro_aire  23
        cuarto_mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.vale03.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.conteo,            
            destino=self.bodega01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=23, # 
            precio_unitario=10.5,
            creador=self.user01,
            observacion="entrada 3er vale"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_twenty_three, #nivel_twenty_three
            movimiento=cuarto_mov_entrada
        )


        #vale04 # bodega01 # SALIDA # nivel_one #filtro_aire  5  (12 + 8 + 15 + 100 = 135 - 5 = 130)
        quinto_mov_salida = MovimientoGeneral.objects.create( 
            vale=self.vale04,
            tipo_movimiento=self.vale04.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega01,            
            destino=self.tractor01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=5, # 
            precio_unitario=10.5,
            creador=self.user01,
            observacion="salida 5to mov"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_one, #nivel_one
            movimiento=quinto_mov_salida
        )

        #vale04 # bodega01 # SALIDA # nivel_twenty_three #filtro_aire  5 ( 23 - 3 )
        sexto_mov_salida = MovimientoGeneral.objects.create(
            vale=self.vale04,
            tipo_movimiento=self.vale04.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega01,            
            destino=self.tractor01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=3, # 
            precio_unitario=10.5,
            creador=self.user01,
            observacion="salida 5to mov"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_twenty_three, #nivel_twenty_three
            movimiento=sexto_mov_salida
        )

        #vale05 # bodega01 # SALIDA # nivel_twenty_three #filtro_aire  7 ( 23 - 3 - 7 = 13 )
        septimo_mov_salida = MovimientoGeneral.objects.create(
            vale=self.vale05,
            tipo_movimiento=self.vale05.tipo_movimiento,
            fecha_movimiento=self.fourfeb,            
            origen=self.bodega01,            
            destino=self.tractor01,            
            producto=self.filtro_aire,
            unidad=self.unidad,
            cantidad=7, # 
            precio_unitario=10.5,
            creador=self.user01,
            observacion="ultima salida 5to mov"
        )
        ProductoExactProfilePosition.objects.create(
            exactposition=self.bodega01_nivel_twenty_three, #nivel_twenty_three
            movimiento=septimo_mov_salida
        )


        exactposition_filtro = self.filtro_aire.what_in_positions_inventory_specific()
        exactposition_producto_x = self.producto_x.what_in_positions_inventory_specific()
        #print(exactposition_filtro)
        self.assertEqual(exactposition_filtro['ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1'], float(130))
        self.assertEqual(exactposition_filtro['ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23'], float(13))
        self.assertEqual(exactposition_producto_x['ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1'], float(500))

        positions_inventory = self.filtro_aire.positions_inventory()
        self.assertEqual(positions_inventory['ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1'], float(630))
        self.assertEqual(positions_inventory['ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23'], float(13))
        #print(positions_inventory)

        #positions = self.filtro_aire.positions()
        #print(positions)

        inventory_filtro = self.filtro_aire.inventory()
        inventory_producto_x = self.producto_x.inventory()
        self.assertEqual(inventory_filtro[0], float(143))
        self.assertEqual(inventory_producto_x[0], float(500))

        exactposition_filtro = self.filtro_aire.what_in_positions_inventory_specific_obj()
        #print(exactposition_filtro)