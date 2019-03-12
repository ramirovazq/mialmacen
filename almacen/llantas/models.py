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


class Movimiento(models.Model):
    tipo_movimiento = models.ForeignKey( #entrada o salida
        TipoMovimiento,
        on_delete=models.PROTECT,
        db_index=True)
    fecha_movimiento = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created
    date_edited = models.DateTimeField(auto_now=True) # Automatically set the field when the object is edited
    no_folio = models.CharField( # Una referencia externa del movimiento
            blank=True,
            null = True,
            max_length=100
    )
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




