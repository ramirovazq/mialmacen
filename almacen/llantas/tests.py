from django.test import TestCase
from django.contrib.auth.models import User

from decimal import Decimal
from .models import *
from .utils import *
from general.models import *

import datetime

class PositionsInventoryTestCase(TestCase):

    def setUp(self):
        self.producto = Producto.objects.create(nombre="Filtro de aire")

        self.user01 = return_profile("rosa")
        self.user02 = return_profile("goyo")

        self.conteo = return_profile("CONTETO", "ABSTRACT")
        self.bodega01 = return_profile("CAJA01", "BODEGA")

        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida = TipoMovimiento.objects.create(nombre="SALIDA")

        tipo_smaller,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="-1")
        tipo_reference, bandera = TipoUnidadMedida.objects.get_or_create(tipo="0")
        tipo_greater,   bandera = TipoUnidadMedida.objects.get_or_create(tipo="1")

        categoria_unidad,   bandera = CategoriaUnidadMedida.objects.get_or_create(nombre="Unidad")

        self.unidad_medida = UnidadMedida.objects.create(
            nombre="unidad",
            categoria=categoria_unidad,
            tipo_unidad=tipo_reference,
            ratio=1,
            simbolo="u"
            )

        self.fourfeb = datetime.datetime.strptime('04/02/2019', "%d/%m/%Y").date()
        self.vale01 = ValeAlmacenGeneral.objects.create(
            no_folio="0001",
            observaciones_grales="nada",
            tipo_movimiento=self.tm_entrada,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )
        self.mov_entrada = MovimientoGeneral.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            producto=self.producto,
            unidad=self.unidad_medida,
            cantidad=10,
            precio_unitario=1.0,
            creador=self.user01
        )
        # position
        bodega_position    = return_position("BODEGA_GRAL")
        self.anaquel_position   = return_position("ANAQUEL", bodega_position)

        # profile
        #self.bodega01 = return_profile("CAJA01", "BODEGA")

        # profile_position
        self.profile_position = ProfilePosition.objects.create(
            profile=self.bodega01, 
            position=self.anaquel_position
        )

        # ProductoExactProfilePosition
        ProductoExactProfilePosition.objects.create(
            exactposition=self.profile_position,
            movimiento=self.mov_entrada
            ) # exactposition = models.ForeignKey(ProfilePosition,
        
        self.lista_ubicaciones = ['1','2','3'] # id_ubicaciones
        self.destino = return_profile("TRACTOR01", "ECONOMICO")# tractor o caja

    def test_simple_position(self):
        self.assertEqual(self.producto.positions_inventory(),{'CAJA01>>BODEGA_GRAL>>ANAQUEL': 10.0})

    def test_position_two_movements(self):

        self.vale02 = ValeAlmacenGeneral.objects.create(
            no_folio="0002",
            observaciones_grales="nada",
            tipo_movimiento=self.tm_salida,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )
        self.mov_salida = MovimientoGeneral.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.destino,
            producto=self.producto,
            unidad=self.unidad_medida,
            cantidad=7,
            precio_unitario=1.0,
            creador=self.user01
        )

        # ProductoExactProfilePosition
        ProductoExactProfilePosition.objects.create(
            exactposition=self.profile_position,
            movimiento=self.mov_salida
            ) # exactposition = models.ForeignKey(ProfilePosition,

        decimal_quantity_3, unidad_medida = self.producto.inventory()
        self.assertEqual(decimal_quantity_3, Decimal('3.0000'))
        self.assertEqual(unidad_medida, self.unidad_medida)
        # (Decimal('3.0000'), <UnidadMedida: unidad (Unidad) [Unidad de Medida de referencia para esta categoria ; 1.00]>)

        self.producto.positions()
        # {<ProfilePosition: CAJA01 [BODEGA] BODEGA_GRAL>>ANAQUEL>}
        self.assertEqual(self.producto.positions_inventory(),{'CAJA01>>BODEGA_GRAL>>ANAQUEL': 3.0})
        self.assertEqual(self.producto.what_in_positions_inventory_specific(),{'CAJA01>>BODEGA_GRAL>>ANAQUEL': Decimal('3.0000')})  












class LlantaMovimientoTestCase(TestCase):
    def setUp(self):

        self.user01 = return_profile("rosa")
        self.user02 = return_profile("goyo")

        self.permis01 = return_profile("susy", "PERMISIONARIO")
        self.permis02 = return_profile("lupita", "PERMISIONARIO")
        self.permis03 = return_profile("rb", "PERMISIONARIO")

        self.conteo = return_profile("CONTETO", "ABSTRACT")
        self.bodega01 = return_profile("CAJA01", "BODEGA")
        self.bodega02 = return_profile("CAJA02", "BODEGA")
        self.tractor01 = return_profile("TRACTOR01", "ECONOMICO")

        ## llanta 01
        self.marca01 = Marca.objects.create(nombre="Michelin", codigo="10")
        self.medida01 = Medida.objects.create(nombre="11R245", codigo="20")
        self.posicion01 = Posicion.objects.create(nombre="T.P.", codigo="30")
        self.status_nueva = Status.objects.create(nombre="Nueva")
        self.status_rodar = Status.objects.create(nombre="Rodar")
        self.porcentaje_rodar_01 = 30
        self.porcentaje_rodar_02 = 50
        self.dot01 = "2323"

        # llanta 02
        self.marca02 = Marca.objects.create(nombre="Goodyear", codigo="11")
        self.medida02 = Medida.objects.create(nombre="11R246", codigo="21")
        self.posicion02 = Posicion.objects.create(nombre="TRACCION", codigo="31")
        #self.status_nueva = Status.objects.create(nombre="Nueva")
        self.dot02 = "2352"

        self.fourfeb = datetime.datetime.strptime('04/02/2019', "%d/%m/%Y").date()

        # se crea una llanta
        self.clase_llanta01 = Llanta.objects.create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_nueva,
            dot=self.dot01,
        )


        self.tm_entrada = TipoMovimiento.objects.create(nombre="ENTRADA")
        self.tm_salida = TipoMovimiento.objects.create(nombre="SALIDA")

        self.vale01 = Vale.objects.create(
            no_folio="0001",
            observaciones_grales="nada",
            tipo_movimiento=self.tm_entrada,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )

        self.vale02 = Vale.objects.create(
            no_folio="0002",
            observaciones_grales="es salida",
            tipo_movimiento=self.tm_salida,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )

        self.vale03 = Vale.objects.create(
            no_folio="0003",
            observaciones_grales="nada",
            tipo_movimiento=self.tm_entrada,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )

        self.vale04 = Vale.objects.create(
            no_folio="0004",
            observaciones_grales="nada",
            tipo_movimiento=self.tm_salida,
            fecha_vale=self.fourfeb,
            persona_asociada=self.user02, # quien entrega
            creador_vale=self.user01,
        )


    def test_add_movimiento(self):

        mov_entrada = Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=5
        )

        mov_entrada_dos = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=2
        )


        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.tractor01,
            llanta=self.clase_llanta01,
            cantidad=4
        )
        
        self.assertEqual(self.clase_llanta01.cantidad_actual_total(), 3)

    def test_bodegas_diferentes(self):
        mov_entrada = Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=5
        )

        mov_entrada_dos = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega02,
            llanta=self.clase_llanta01,
            cantidad=2
        )

        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.tractor01,
            llanta=self.clase_llanta01,
            cantidad=1
        )

        self.assertEqual(self.clase_llanta01.total_ubicaciones(), {"CAJA01": 4, "CAJA02":2})


    def test_movimientos_restantes(self):

        mov_entrada = Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=5
        )

        mov_entrada_dos = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=2
        )

        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.tractor01,
            llanta=self.clase_llanta01,
            cantidad=1
        )
        parametro_busqueda = self.dot01#self.dot01 = "2323"
        llantas_busqueda = Llanta.objects.filter(dot__icontains=parametro_busqueda )

        llanta = llantas_busqueda[0]
        self.assertEqual(llanta.total_ubicaciones(), {"CAJA01": 6})

        mov_salida_dos = Movimiento.objects.create(
            vale=self.vale04,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01, # CAJA01
            destino=self.tractor01,
            llanta=llanta,
            cantidad=4
        )
        self.assertEqual(llanta.total_ubicaciones(), {"CAJA01": 2})

    def test_add_llanta_rodar(self):

        ## en setup
        self.clase_llanta01

        # se crea una llanta rodar 01
        self.llanta_rodar_01, bandera_rodar_01 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=self.porcentaje_rodar_01 #30
            
        )

        # se crea una llanta rodar 02
        self.llanta_rodar_02, bandera_rodar_02 = Llanta.objects.get_or_create(
            marca=self.marca02,
            medida=self.medida02,
            posicion=self.posicion02,
            status=self.status_rodar,
            dot= self.dot02,
            porciento_vida=self.porcentaje_rodar_02
 
        )

        # se crea una llanta rodar 03 similar a 01
        self.llanta_rodar_03, bandera_rodar_03 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=60 # en esto difiere de self.porcentaje_rodar_01
 
        )

        # se crea una llanta rodar 04 Equal to 01
        self.llanta_rodar_04, bandera_rodar_01 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=self.porcentaje_rodar_01 #30
            
        )

        self.assertEqual(len(Llanta.objects.all()), 4)

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=1
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_01,
            cantidad=2
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_02,
            cantidad=1

        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_03,
            cantidad=5
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_04,
            cantidad=3
        )

        self.assertEqual(self.clase_llanta01.cantidad_actual_total(), 1)
        self.assertEqual(self.llanta_rodar_01.cantidad_actual_total(), 5)
        self.assertEqual(self.llanta_rodar_02.cantidad_actual_total(), 1)
        self.assertEqual(self.llanta_rodar_03.cantidad_actual_total(), 5)
        self.assertEqual(self.llanta_rodar_04.cantidad_actual_total(), 5)

    def test_permisionarios(self):

        mov_entrada = Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.clase_llanta01,
            cantidad=3
        )

        mov_entrada_dos = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega02,
            llanta=self.clase_llanta01,
            cantidad=5,
            permisionario=self.permis01
        )

        mov_entrada_tres = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega02,
            llanta=self.clase_llanta01,
            cantidad=2,
            permisionario=self.permis02
        )

        mov_entrada_cuatro = Movimiento.objects.create(
            vale=self.vale03,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega02,
            llanta=self.clase_llanta01,
            cantidad=3
        )


        ## SALIDAS
        ### SALIDA BODEGA 1
        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.tractor01,
            llanta=self.clase_llanta01,
            cantidad=1
        )

        ### SALIDA BODEGA 2
        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega02,
            destino=self.tractor01,
            llanta=self.clase_llanta01,
            cantidad=2,
            permisionario=self.permis02
        )

        self.assertEqual(self.clase_llanta01.cantidad_actual_total(), 10)
        self.assertEqual(self.clase_llanta01.total_ubicaciones_detail(), 
            {
            "CAJA01": {'sin_permisionario': 2}, 
            "CAJA02": {'sin_permisionario':3, 
                       self.permis01.user.username:5}
            })




    def test_llanta_rodar_y_permisionarios(self):

        # se crea una llanta rodar 01
        self.llanta_rodar_01, bandera_rodar_01 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=self.porcentaje_rodar_01 #30
            
        )

        # se crea una llanta rodar 02
        self.llanta_rodar_02, bandera_rodar_02 = Llanta.objects.get_or_create(
            marca=self.marca02,
            medida=self.medida02,
            posicion=self.posicion02,
            status=self.status_rodar,
            dot= self.dot02,
            porciento_vida=self.porcentaje_rodar_02
 
        )

        # se crea una llanta rodar 03 similar a 01
        self.llanta_rodar_03, bandera_rodar_03 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=60 # en esto difiere de self.porcentaje_rodar_01
 
        )

        # se crea una llanta rodar 04 Equal to 01
        self.llanta_rodar_04, bandera_rodar_01 = Llanta.objects.get_or_create(
            marca=self.marca01,
            medida=self.medida01,
            posicion=self.posicion01,
            status=self.status_rodar,
            dot=self.dot01,
            porciento_vida=self.porcentaje_rodar_01 #30
            
        )

        self.assertEqual(len(Llanta.objects.all()), 4)

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_01,
            cantidad=2,
            permisionario=self.permis01
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_01,
            cantidad=3,
            permisionario=self.permis02
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_02,
            cantidad=1,
            permisionario=self.permis01

        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_03,
            cantidad=5,
            permisionario=self.permis01
        )

        Movimiento.objects.create(
            vale=self.vale01,
            tipo_movimiento=self.tm_entrada,
            fecha_movimiento=self.fourfeb,
            origen=self.conteo,
            destino=self.bodega01,
            llanta=self.llanta_rodar_04,
            cantidad=3,
            permisionario=self.permis01
        )

        
        self.assertEqual(self.llanta_rodar_01.cantidad_actual_total(), 8)
        self.assertEqual(self.llanta_rodar_02.cantidad_actual_total(), 1)
        self.assertEqual(self.llanta_rodar_03.cantidad_actual_total(), 5)
        self.assertEqual(self.llanta_rodar_04.cantidad_actual_total(), 8)


        ### SALIDA BODEGA 1
        mov_salida = Movimiento.objects.create(
            vale=self.vale02,
            tipo_movimiento=self.tm_salida,
            fecha_movimiento=self.fourfeb,
            origen=self.bodega01,
            destino=self.tractor01,
            llanta=self.llanta_rodar_01,
            cantidad=2,
            permisionario=self.permis02
        )

        self.assertEqual(self.llanta_rodar_01.total_ubicaciones_detail(), 
            {
            "CAJA01": {'sin_permisionario': 0, self.permis01.user.username:5, self.permis02.user.username:1}
            })

        self.assertEqual(self.llanta_rodar_02.total_ubicaciones_detail(), 
            {
            "CAJA01": {'sin_permisionario': 0, self.permis01.user.username:1}
            })

        self.assertEqual(self.llanta_rodar_03.total_ubicaciones_detail(), 
            {
            "CAJA01": {'sin_permisionario': 0, self.permis01.user.username:5}
            })
