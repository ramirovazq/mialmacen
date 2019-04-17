from rest_framework import serializers
from llantas.models import Vale

class ValeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vale
        fields = '__all__'
