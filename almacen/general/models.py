from django.db import models
from persona.models import Profile, ProfilePosition
from llantas.models import TipoMovimiento, Vale  # catálogo de tipos de movimiento, ENTRADA, SALIDA

import decimal

class TipoUnidadMedida(models.Model): # smaller, reference, greater
    SMALLER_REFERENCE_UNIT = '-1'
    REFERENCE_UNIT = '0'
    GREATER_REFERENCE_UNIT = '1'
    REFERENCE_CHOICES = [
        (SMALLER_REFERENCE_UNIT , 'Mas pequeña que la unidad de medida de referencia'),
        (REFERENCE_UNIT , 'Unidad de Medida de referencia para esta categoria'),
        (GREATER_REFERENCE_UNIT, 'Mas grande que la unidad de medida de referencia'),
    ]

    tipo = models.CharField(
        max_length=2,
        choices=REFERENCE_CHOICES,
        default=REFERENCE_UNIT,
    )

    def __str__(self):
        return "{}".format(self.tipo)


    def words(self):
        #REFERENCE_CHOICES. self.tipo
        return [x for x in self.REFERENCE_CHOICES if x[0] == self.tipo][0][1]


class CategoriaUnidadMedida(models.Model): # Longitud/Distancia, Unidad, Volumen, Pes, Horario de trabajo
    nombre = models.CharField( 
            blank=True,
            null = True,
            max_length=30
    )

    def __str__(self):
        return "{}".format(self.nombre)


class UnidadMedida(models.Model): # cm, kg, km, Litro, etc
    nombre = models.CharField( 
            blank=True,
            null = True,
            max_length=30
    )

    categoria = models.ForeignKey(  # Longitud/Distancia, Unidad, Volumen, Pes, Horario de trabajo
        CategoriaUnidadMedida,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    tipo_unidad = models.ForeignKey(  # smaller, reference, greater
        TipoUnidadMedida,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    ratio = models.DecimalField( # por ejemplo, si estamos creando la caja con 6 unidades ... se pone 6
        max_digits=8,   
        decimal_places=2,
        default=1)


    simbolo = models.CharField( 
            blank=True,
            null = True,
            max_length=10
    )


    def __str__(self):
        return "{} ({}) [{} ; {}]".format(self.nombre, self.categoria, self.tipo_unidad.words(), self.ratio)


class ValeAlmacenGeneral(Vale): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    pass

    def movimientos(self):
        return MovimientoGeneral.objects.filter(vale=self)

    def total(self):
        return sum([m.precio_total() for m in self.movimientos()])



class Producto(models.Model):
    nombre = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank=True,
            null = True,
            max_length=250
    )

    def devuelve_unidad_referencia(self, movimiento=None):
        unidad_referencia = None
        tipo_referencia = TipoUnidadMedida.objects.get(tipo=0) # reference
        if movimiento:
            unidad = movimiento.unidad
            la_categoria = unidad.categoria
        else:
            movimientos = MovimientoGeneral.objects.filter(producto=self)
            if movimientos.exists():
                movimiento = movimientos[0]
                unidad = movimiento.unidad
                la_categoria = unidad.categoria
            else:
                la_categoria = None

        unidad_queryset = UnidadMedida.objects.filter(
            categoria=la_categoria,
            tipo_unidad=tipo_referencia
        )
        if len(unidad_queryset) > 0:
            unidad_referencia = unidad_queryset[0] 
        return unidad_referencia


    def movimientos(self, tipo="ENTRADA", origen=None, destino=None): # can or cant no specigy destino
        tipo_movimiento = TipoMovimiento.objects.get(nombre=tipo)

        dict_query = {}
        dict_query['tipo_movimiento'] = tipo_movimiento
        dict_query['producto']        = self

        if origen:
            dict_query['origen'] = origen
        if destino:
            dict_query['destino'] = destino


        movimientos = MovimientoGeneral.objects.filter(
            **dict_query
            )
        return movimientos

    def movimientos_entrada(self):
        return self.movimientos("ENTRADA")

    def movimientos_salida(self):
        return self.movimientos("SALIDA")


    def inventory(self, lugar=None):

        movimientos_entrada = self.movimientos("ENTRADA", destino=lugar)
        movimientos_salida  = self.movimientos("SALIDA", origen=lugar)

        try:
            primer_movimiento = movimientos_entrada[0]
            unidad_referencia = self.devuelve_unidad_referencia(primer_movimiento)
        except IndexError:
            unidad_referencia = None

        total_entrada = 0
        total_salida  = 0

        for m_entrada in movimientos_entrada:
            total_entrada = total_entrada + (m_entrada.cantidad*m_entrada.unidad.ratio)

        for m_salida in movimientos_salida:
            total_salida = total_salida + (m_salida.cantidad*m_salida.unidad.ratio)

        return total_entrada-total_salida, unidad_referencia

    def positions(self, lugar=None):
        movimientos_entrada = self.movimientos("ENTRADA", destino=lugar)
        answer = set()
        for movimiento_e in movimientos_entrada:
            list_exactpositions = [x.exactposition for x in ProductoExactProfilePosition.objects.filter(movimiento=movimiento_e)]
            if len(list_exactpositions) > 0:
                answer.add(list_exactpositions[0])
        '''
        answer, set of exactposition, que es un ProfilePosition
            class ProfilePosition(models.Model):
                 profile = models.ForeignKey( # self.bodega01 = return_profile("ALMACEN_GENERAL", "BODEGA")
                 Profile,
                )
                position = models.ForeignKey( # nivel_one = Position.objects.create(name="Nivel de Anaquel 1", parent=anaquel_one)
                Position,
                )
        example: {<ProfilePosition: ALMACEN_GENERAL [BODEGA] Anaquel 1>>Nivel de Anaquel 1>, <ProfilePosition: ALMACEN_GENERAL [BODEGA] Anaquel 1>>Nivel de Anaquel 23>}
        '''
        return answer


    def positions_inventory(self, lugar=None):
        '''
        regresa un dicc
        llaves: las posiciones exactas en donde estan los productos
        valor: el totalde elementos que estan en las posiciones exactas
        # producto_X
        example: {'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1': 630.0, 'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23': 13.0}
        '''
        answer = {}
        set_positions_entrada = self.positions(lugar) #ProfilePosition
        for profileposition in set_positions_entrada:
            answer[profileposition.in_words()] = 0
            total_entrada = 0
            total_salida  = 0
            for x in ProductoExactProfilePosition.objects.filter(exactposition=profileposition):
                if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                    total_entrada = total_entrada + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
                elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                    total_salida = total_salida + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
            answer[profileposition.in_words()] = float(total_entrada-total_salida)
        # returns {'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1': 630.0, 'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23': 13.0}
        return answer


    def what_in_positions_inventory(self, lugar=None):
        #movimientos_salida = self.movimientos("SALIDA", destino=lugar)
        answer = {}
        set_positions_entrada = self.positions(lugar) #ProfilePosition
        for profileposition in set_positions_entrada:
            answer[profileposition.in_words()] = 0
            total_entrada = 0
            total_salida  = 0
            answer[profileposition.in_words()] = ProductoExactProfilePosition.objects.filter(exactposition=profileposition)
        '''
            answer = {
                'BODEGA_GENERAL>>ANAQUEL 19>>NIVEL DE ANAQUEL 10': 
                <QuerySet [
                    <ProductoExactProfilePosition: BODEGA_GENERAL [BODEGA] ANAQUEL 19>>NIVEL DE ANAQUEL 10 3935>, 
                    <ProductoExactProfilePosition: BODEGA_GENERAL [BODEGA] ANAQUEL 19>>NIVEL DE ANAQUEL 10 3936>, 
                    <ProductoExactProfilePosition: BODEGA_GENERAL [BODEGA] ANAQUEL 19>>NIVEL DE ANAQUEL 10 3937>, 
                    <ProductoExactProfilePosition: BODEGA_GENERAL [BODEGA] ANAQUEL 19>>NIVEL DE ANAQUEL 10 3938>]>, 
                'OFICINA_CONTADOR>>ANAQUEL 1>>NIVEL DE ANAQUEL 1': 
                <QuerySet [
                    <ProductoExactProfilePosition: OFICINA_CONTADOR [BODEGA] ANAQUEL 1>>NIVEL DE ANAQUEL 1 4448>, 
                    <ProductoExactProfilePosition: OFICINA_CONTADOR [BODEGA] ANAQUEL 1>>NIVEL DE ANAQUEL 1 4449>,
                    <ProductoExactProfilePosition: OFICINA_CONTADOR [BODEGA] ANAQUEL 1>>NIVEL DE ANAQUEL 1 4450>, 
                    <ProductoExactProfilePosition: OFICINA_CONTADOR [BODEGA] ANAQUEL 1>>NIVEL DE ANAQUEL 1 4457>, 
                    <ProductoExactProfilePosition: OFICINA_CONTADOR [BODEGA] ANAQUEL 1>>NIVEL DE ANAQUEL 1 4526>]>}

            class ProductoExactProfilePosition(models.Model):
                exactposition = models.ForeignKey(
                    ProfilePosition,
                )
                movimiento = models.ForeignKey(
                    MovimientoGeneral,
                )
        '''
        return answer


    def what_in_positions_inventory_specific(self):
        '''
        returns
        example: {'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1': Decimal('130.0000'), 'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23': Decimal('13.0000')}
        '''
        answer = {}
        total_entrada = 0
        total_salida  = 0
        dicc_y = self.what_in_positions_inventory() # answer["OFICINA_CONTADOR>>ANAQUEL 1>>NIVEL DE ANAQUEL 1"] = <QuerySet [<ProductoExactProfilePosition: BODEGA_GENE

        for llave_y in dicc_y:
            productexactprofileposition = dicc_y[llave_y] # productexactprofileposition

            total_entrada = 0
            total_salida  = 0

            for  x in productexactprofileposition:
                if x.movimiento.producto == self:
                    if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                        total_entrada = total_entrada + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
                    elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                        total_salida = total_salida + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
                answer[x.exactposition.in_words()] = total_entrada - total_salida
        return answer


    def what_in_positions_inventory_specific_obj(self):
        '''
        too similiar to what_in_positions_inventory_specific
        but in key returns <ProfilePosition object>
        is better when rendering template
        returns
        example: {<ProfilePosition: ALMACEN_GENERAL [BODEGA] Anaquel 1>>Nivel de Anaquel 1>: Decimal('130.0000'), <ProfilePosition: ALMACEN_GENERAL [BODEGA] Anaquel 1>>Nivel de Anaquel 23>: Decimal('13.0000')}
        '''
        answer = {}
        total_entrada = 0
        total_salida  = 0
        dicc_y = self.what_in_positions_inventory() # answer["OFICINA_CONTADOR>>ANAQUEL 1>>NIVEL DE ANAQUEL 1"] = <QuerySet [<ProductoExactProfilePosition: BODEGA_GENE

        for llave_y in dicc_y:
            productexactprofileposition = dicc_y[llave_y] # productexactprofileposition

            total_entrada = 0
            total_salida  = 0

            for  x in productexactprofileposition:
                if x.movimiento.producto == self:
                    if x.movimiento.tipo_movimiento.nombre == 'ENTRADA':
                        total_entrada = total_entrada + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
                    elif x.movimiento.tipo_movimiento.nombre == 'SALIDA':
                        total_salida = total_salida + (x.movimiento.cantidad*x.movimiento.unidad.ratio)
                answer[x.exactposition] = total_entrada - total_salida
        return answer


    def __str__(self):
        return "{} (id, {})".format(self.nombre, self.id)


class MovimientoGeneral(models.Model):
    vale = models.ForeignKey(
        ValeAlmacenGeneral,
        related_name='vale_almacengeneral_asociado',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)
    fecha_movimiento = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    date_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited
    origen = models.ForeignKey(
        Profile,
        related_name='origen_del_movimiento_almacengeneral',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    destino = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='destino_del_movimiento_almacengeneral',
        on_delete=models.PROTECT,
        db_index=True)

    producto = models.ForeignKey(
        Producto,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    unidad = models.ForeignKey( 
        UnidadMedida,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)


    cantidad = models.DecimalField(
        max_digits=8,   
        decimal_places=2,
        default=0)

    precio_unitario = models.DecimalField(
        max_digits=8,   
        decimal_places=2,
        default=0)

    creador = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creadror_del_movimiento_almacengeneral',
        on_delete=models.PROTECT,
        db_index=True)

    observacion = models.TextField(
        blank=True,
        null=True
    )

    def le_positions(self):
        return ProductoExactProfilePosition.objects.filter(movimiento=self)

    def list_exact_positions(self):
        l = []
        for x in self.le_positions():
            l.append(x.exactposition)
        return l



    def precio_total(self):
        if self.vale.con_iva:
            return (self.cantidad * self.precio_unitario) + ((self.cantidad * self.precio_unitario) * decimal.Decimal(0.16))        
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return "{}".format(self.id)

    @staticmethod
    def entradas(dot=""):
        tme = TipoMovimiento.objects.get(nombre="ENTRADA")
        if dot:
            return MovimientoGeneral.objects.filter(tipo_movimiento=tme)
        else:
            return MovimientoGeneral.objects.filter(tipo_movimiento=tme)

    @staticmethod
    def salidas(dot=""):
        tms = TipoMovimiento.objects.get(nombre="SALIDA")
        if dot:
            return MovimientoGeneral.objects.filter(tipo_movimiento=tme)
        else:
            return MovimientoGeneral.objects.filter(tipo_movimiento=tms)



class ProductoExactProfilePosition(models.Model):
    exactposition = models.ForeignKey(
        ProfilePosition,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="productoexactprofileposition_exactposition",
    )
    movimiento = models.ForeignKey(
        MovimientoGeneral,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="productoexactprofileposition_movimiento",
    )

    def __str__(self):
        return "{} {}".format(self.exactposition, self.movimiento)
