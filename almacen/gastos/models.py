from django.db import models
from django.contrib.auth.models import User

# diversion, transporte, vivienda, comida, generales
class CategoriaGastos(models.Model): 
    categoria = models.CharField( 
            blank=True,
            null = True,
            max_length=50
    )

    def __str__(self):
        return "{}".format(self.categoria)

class Gasto(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.PROTECT
    )
    concepto = models.CharField( 
            max_length=100
    )
    monto = models.DecimalField(
        max_digits=8,   
        decimal_places=2,
        default=0
    )
    fecha = models.DateField(
        blank=True,
        null=True
    )
    fecha_created = models.DateTimeField(
        auto_now_add=True
    )
    categoria = models.ForeignKey(
        CategoriaGastos,
        blank=True,
        null=True,        
        related_name='categoria_del_gasto',
        on_delete=models.PROTECT,
        db_index=True)

    def __str__(self):
        return f"{self.id} {self.concepto} {self.monto} {self.user.username}"

