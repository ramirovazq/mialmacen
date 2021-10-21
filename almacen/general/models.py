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

    @staticmethod
    def generate_authomatic(usuario, tipo_movimiento="SALIDA"):
        from datetime import datetime
        from llantas.utils import return_existent_profile

        hoy_datetime  = datetime.today()
        no_folio = hoy_datetime.strftime("%d/%m/%Y-%H%M%S")
        hoy = hoy_datetime.date()
        tm = TipoMovimiento.objects.get(nombre=tipo_movimiento)
        flag, profile_request =  return_existent_profile(usuario)
        if flag:
            vale = ValeAlmacenGeneral.objects.create(
                no_folio = no_folio,
                observaciones_grales="{} lector".format(tipo_movimiento),
                tipo_movimiento= tm,
                fecha_vale=hoy,
                persona_asociada=profile_request,
                creador_vale=profile_request,
                con_iva=True,
                vale_llantas=False
            )
            return vale
        return None


    def movimientos_authomatic_from_list_products(self, list_ids_products, origen_id, destino_id, profile_positions, unidad_id=None):
        '''
        list_ids_products
        [{'70': Decimal('1.0000')}, 
         {'23': Decimal('2.0000')}, ...  {'id_producto': Decimal('quantity_i_want')}]
         profile_position = [<ProfilePosition: CAJA01 [BODEGA] BODEGA_GRAL>>ANAQUEL>,
                 <ProfilePosition: CAJA01 [BODEGA] BODEGA_GRAL>>ANAQUEL2>]
        '''
        o = Profile.objects.get(id=origen_id)
        d = Profile.objects.get(id=destino_id)

        for zip_var in zip(list_ids_products, profile_positions):
            dict_product_i_want = zip_var[0]
            profile_position    = zip_var[1]

            id_producto_ = [int(x) for x in dict_product_i_want.keys()]
            id_producto = id_producto_[0]

            quantity_producto = dict_product_i_want[str(id_producto)]

            p = Producto.objects.get(id=id_producto)
            if unidad_id:
                unidad = UnidadMedida.objects.get(
                    id=unidad_id
                )
                u = unidad
            else:
                u = p.devuelve_unidad_referencia()

            last_product_price = p.last_not_zero_purchase_price()
            m = MovimientoGeneral.objects.create(
                vale = self,
                tipo_movimiento = self.tipo_movimiento,
                fecha_movimiento = self.fecha_vale,
                origen=o,
                destino=d,
                producto=p,
                unidad=u,
                cantidad=quantity_producto,
                precio_unitario=last_product_price,
                creador=self.creador_vale,
                observacion="movimiento desde lector o app",
            )
            
            ProductoExactProfilePosition.objects.create(
                exactposition=profile_position,
                movimiento=m
            )
        return None


class Producto(models.Model):
    nombre = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank=True,
            null = True,
            max_length=250
    )
    maximum = models.PositiveIntegerField(
            default=0
    )
    minimum = models.PositiveIntegerField(
            default=0
    )

    class Meta:
        unique_together = (('nombre',
        ))

    def last_purchase_price(self):
        tm_entrada, _ = TipoMovimiento.objects.get_or_create(nombre="ENTRADA")
        movimientos = MovimientoGeneral.objects.filter(
            tipo_movimiento=tm_entrada,
            producto=self,
        ).order_by('-date_created')
        if len(movimientos) == 0:
            return 0
        last_movimiento = movimientos[0]
        return last_movimiento.precio_unitario

    def last_not_zero_purchase_price(self):
        tm_entrada, _ = TipoMovimiento.objects.get_or_create(nombre="ENTRADA")
        movimientos = MovimientoGeneral.objects.filter(
            tipo_movimiento=tm_entrada,
            producto=self,
        ).order_by('-date_created')

        if len(movimientos) == 0:
            return 0

        last_price = 0
        for movimiento in movimientos:
            if movimiento.precio_unitario > 0:
                return movimiento.precio_unitario
        return last_price


    def avg_purchase_price(self):
        tm_entrada, _ = TipoMovimiento.objects.get_or_create(nombre="ENTRADA")
        movimientos = MovimientoGeneral.objects.filter(
            tipo_movimiento=tm_entrada,
            producto=self,
        ).order_by('-date_created')
        number_movimientos = len(movimientos)
        if number_movimientos == 0:
            return 0
        sum_prices = sum([movimiento.precio_unitario for movimiento in movimientos])
        return sum_prices / number_movimientos



    def alarm_maximum_and_minimum(self):
        actual_quantity = self.inventory()[0]
        return not(self.minimum < actual_quantity <= self.maximum)

    def alarm_minimum(self):
        actual_quantity = self.inventory()[0]
        return not(self.minimum < actual_quantity)

    def alarm_maximum(self):
        actual_quantity = self.inventory()[0]
        return not(actual_quantity < self.maximum)


    def numeros_de_parte(self):
        return NumeroParte.objects.filter(producto=self)

    def numeros_de_parte_format(self):
        return ["[{}]".format(x.numero_de_parte) for x in self.numeros_de_parte()]
        
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
        return self.movimientos("ENTRADA").order_by('-date_created')

    def movimientos_salida(self):
        return self.movimientos("SALIDA").order_by('-date_created')


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

    def inventory_words(self, lugar=None):

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

        if unidad_referencia:
            return {"total": total_entrada-total_salida, "unidad_referencia":unidad_referencia.simbolo}
        else:
            return {"total": total_entrada-total_salida, "unidad_referencia": "?"}


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
        example: {'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 1': Decimal('130.0000'), 
                 'ALMACEN_GENERAL>>Anaquel 1>>Nivel de Anaquel 23': Decimal('13.0000')}
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
        cadena = ""
        cadena = "{} {}".format(self.id, self.nombre)
        if len(self.numeros_de_parte()) > 0:
            return cadena + " "+ ";".join(self.numeros_de_parte_format())
        else:
            return cadena

class NumeroParte(models.Model):
    producto = models.ForeignKey( # AmerSteel, Dunlop, Michellin, etc
            Producto,
            related_name='producto_numero_de_parte',
            on_delete=models.PROTECT,
            blank=False,
            null=False,
            db_index=True)

    numero_de_parte = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank = False,
            null = False,
            max_length=70
    )
    class Meta:
        unique_together = (('producto', 'numero_de_parte'))
        



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
