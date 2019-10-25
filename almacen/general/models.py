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


class Producto(models.Model):
    nombre = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank=True,
            null = True,
            max_length=250
    )

    def devuelve_unidad_referencia(self, movimiento):
        unidad_referencia = None
        tipo_referencia = TipoUnidadMedida.objects.get(tipo=0) # reference
        unidad = movimiento.unidad
        la_categoria = unidad.categoria

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
        '''
        return answer


    def positions_inventory(self, lugar=None):
        #movimientos_salida = self.movimientos("SALIDA", destino=lugar)
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
