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

class Position(models.Model):
    name = models.CharField( #anaquel 1 
            blank=True,
            null = True,
            max_length=70
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        db_index=True,
        related_name="parent_position",
        null=True,
        blank=True
        )

    def __str__(self):
        if self.parent:
            return "{}>>{}".format(self.parent, self.name)
        else:
            return "{}".format(self.name)

class ProfilePosition(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="profileposition_profile_set",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="profileposition_position_set",
    )

    def __str__(self):
        return "{} {}".format(self.profile, self.position)

    def in_words(self):
        bodega = "{}>>{}".format(self.profile.user.username, self.position.__str__())
        return bodega

