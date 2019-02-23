#from django.contrib.auth.models import User
#from django.conf import settings
from django.db import models
#from datetime import date

class Marca(models.Model):
    nombre = models.CharField(
            blank=True,
            null = True,
            max_length=100
    )

    def __str__(self):
        return "{}".format(self.nombre)
