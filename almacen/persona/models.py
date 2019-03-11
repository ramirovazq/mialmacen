from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=70
    )

    def __str__(self):
        return "{}".format(self.nombre)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tipo = models.ForeignKey(
        Tipo,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tipo_profile"
    )

    def __str__(self):
        return "{} [{}]".format(self.user, self.tipo)

