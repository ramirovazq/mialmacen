from django.db import models

# Create your models here.
class Vehicle(models.Model):

    vehicle_make = models.CharField(
            verbose_name='Make',
            blank=False,
            null = True,
            max_length=300
    )

    vehicle_model = models.CharField(
            verbose_name='Model',
            blank=False,
            null = True,
            max_length=300
    )

    description = models.TextField(
            blank=False,
            null = True,
    )

    color = models.CharField(
            blank=False,
            null = True,
            max_length=300
    )

    doors = models.PositiveSmallIntegerField(
            blank=False,
            null = False,
            default=2
    )

    lot_number = models.CharField(
            verbose_name='Lot #',
            blank=False,
            null = True,
            max_length=300
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return "{} {}, color {}, doors {}".format(self.vehicle_make, self.vehicle_model, self.color, self.doors)

