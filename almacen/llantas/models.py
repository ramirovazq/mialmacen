from django.db import models
from persona.models import Profile

class Marca(models.Model): 
    nombre = models.CharField( # AmerSteel, Dunlop, Michellin, etc
            blank=True,
            null = True,
            max_length=100
    )

    codigo = models.CharField( #11,12,13, etc
            max_length=30,
            unique=True
    )


    def __str__(self):
        return "{} [{}]".format(self.nombre, self.codigo)

class Medida(models.Model): 
    nombre = models.CharField( # 11R225, 11R245, 15R225
            blank=True,
            null = True,
            max_length=100
    )

    codigo = models.CharField( #21, 22, 23 etc
            max_length=30,
            unique=True
    )

    class Meta:
        verbose_name_plural = "medidas"

    def __str__(self):
        return "{} [{}]".format(self.nombre, self.codigo)


class Posicion(models.Model): 
    nombre = models.CharField( # T.P, Tracción
            blank=True,
            null = True,
            max_length=100
    )

    codigo = models.CharField( #31, 32, etc
            max_length=30,
            unique=True
    )

    class Meta:
        verbose_name_plural = "posiciones"

    def __str__(self):
        return "{} [{}]".format(self.nombre, self.codigo)


class Status(models.Model): 
    nombre = models.CharField( # Nueva, Renovada, Rodar
            blank=True,
            null = True,
            max_length=100
    )

    class Meta:
        verbose_name_plural = "status"


    def __str__(self):
        return "{}".format(self.nombre)


class TipoMovimiento(models.Model): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    nombre = models.CharField( # Nueva, Renovada, Rodar
            blank=True,
            null = True,
            max_length=100
    )

    class Meta:
        verbose_name_plural = "tipo de movimientos"

    def __str__(self):
        return "{}".format(self.nombre)

class Vale(models.Model): # catálogo de tipos de movimiento, ENTRADA, SALIDA
    no_folio = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100
    )

    observaciones_grales = models.TextField(
        blank=True,
        null=True
    )

    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True)

    fecha_vale = models.DateField()
    fecha_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    fecha_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited

    persona_asociada = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='persona_asociada',
        on_delete=models.PROTECT,
        db_index=True)

    creador_vale = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creador_vale',
        on_delete=models.PROTECT,
        db_index=True)


    class Meta:
        verbose_name_plural = "Vales"

    def __str__(self):
        return "{}".format(self.no_folio)



class Movimiento(models.Model):
    vale = models.ForeignKey(
        Vale,
        related_name='vale_asociado',
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
        related_name='origen_del_movimiento',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True)
    destino = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='destino_del_movimiento',
        on_delete=models.PROTECT,
        db_index=True)

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_index=True)
    medida = models.ForeignKey(
        Medida,
        on_delete=models.PROTECT,
        db_index=True)
    posicion = models.ForeignKey(
        Posicion,
        on_delete=models.PROTECT,
        db_index=True)
    cantidad = models.PositiveIntegerField(
            default=0)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        db_index=True)
    dot = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100)
    precio_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0)

    creador = models.ForeignKey(
        Profile,
        blank=True,
        null=True,        
        related_name='creadror_del_movimiento',
        on_delete=models.PROTECT,
        db_index=True)


    def sku(self):
        return "{}{}{}".format(self.marca.codigo,self.medida.codigo, self.posicion.codigo)

    def __str__(self):
        return "{}".format(self.id)

    @staticmethod
    def entradas(dot=""):
        tme = TipoMovimiento.objects.get(nombre="ENTRADA")
        if dot:
            return Movimiento.objects.filter(tipo_movimiento=tme, dot=dot)
        else:
            return Movimiento.objects.filter(tipo_movimiento=tme)

    @staticmethod
    def salidas(dot=""):
        tms = TipoMovimiento.objects.get(nombre="SALIDA")
        if dot:
            return Movimiento.objects.filter(tipo_movimiento=tme, dot=dot)
        else:
            return Movimiento.objects.filter(tipo_movimiento=tms)

    @classmethod
    def give_unique(self, query_movimiento, orden='marca'): 
        '''
        devuelve un diccionario y un set  
        el diccionario tiene la llave de la huella de la llanta (huella es marca__medida__posicion__dot)
        y como valor, la cantidad de llantas
        el set del diccionario
        '''
        dicc = {}
        for m in query_movimiento:
            if orden == 'marca':
                llanta_name = "{}__{}__{}__{}".format(m.marca.nombre, m.medida.nombre, m.posicion.nombre, m.dot)
            elif orden == 'medida':
                llanta_name = "{}__{}__{}__{}".format(m.medida.nombre, m.posicion.nombre, m.dot, m.marca.nombre)
            elif orden == 'posicion':
                llanta_name = "{}__{}__{}__{}".format(m.posicion.nombre, m.dot, m.marca.nombre, m.medida.nombre)
            elif orden == 'dot':
                llanta_name = "{}__{}__{}__{}".format(m.dot, m.marca.nombre, m.medida.nombre, m.posicion.nombre)
            else:
                llanta_name = "{}__{}__{}__{}".format(m.marca.nombre, m.medida.nombre, m.posicion.nombre, m.dot)


            if llanta_name not in dicc.keys():
                dicc[llanta_name] = m.cantidad
            else:
                dicc[llanta_name] = dicc[llanta_name] + m.cantidad        
        #lista = sorted(dicc.items(), key=lambda x: x[1]) 
        #lista.reverse()
        unique = set(dicc)
        return dicc, unique

    @classmethod
    def actual_inventory(self, orden='marca', dot=""):
        if dot:
            dicc_entradas, unique_entradas = self.give_unique(self.entradas(dot), orden)
            dicc_salidas, unique_salidas   = self.give_unique(self.salidas(dot), orden)
        else:
            dicc_entradas, unique_entradas = self.give_unique(self.entradas(), orden)
            dicc_salidas, unique_salidas   = self.give_unique(self.salidas(), orden)
        actual = {}

        # set operation
        salidas_sin_entradas = unique_salidas.difference(unique_entradas)        

        for huella in dicc_entradas.keys():
            actual[huella] = 0
            try:
                num_actual_entrada = dicc_entradas[huella]                
            except KeyError:
                num_actual_entrada = 0
                #print("doesnt find huella in dictionary ENTRADA")                
            try:
                num_actual_salida = dicc_salidas[huella]
            except KeyError:
                num_actual_salida = 0
                #print("doesnt find huella in dictionary SALIDA")

            actual[huella] = num_actual_entrada - num_actual_salida

        lista = actual.items()
        #lista = sorted(actual.items(), key=lambda x: x[1]) 
        #lista.reverse()
        return actual, lista, salidas_sin_entradas