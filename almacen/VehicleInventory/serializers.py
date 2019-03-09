from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('vehicle_make', 'vehicle_model', 'description', 'color', 'doors', 'lot_number')