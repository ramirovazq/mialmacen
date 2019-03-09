#from django.contrib.auth.models import User
#from django.conf import settings
from django.db import models
#from datetime import date

class Tipo(models.Model): ## marca, medida, tipo, Status
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=70
    )

    def __str__(self):
        return "{}".format(self.nombre)




class Clasificacion(models.Model):
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=100
    )
    codigo = models.CharField(
            blank=True,
            null = True,
            max_length=30
    )
    tipo = models.ForeignKey(
        Tipo,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tipo_clasificacion"
    )


    def __str__(self):
        return "{} {}".format(self.nombre, self.codigo)
