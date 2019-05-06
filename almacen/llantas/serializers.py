from rest_framework import serializers
from llantas.models import Vale, Llanta, Marca, Medida, Posicion, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class LlantaSerializer(serializers.ModelSerializer):
    marca    = MarcaSerializer(read_only=True)
    medida   = MedidaSerializer(read_only=True)
    posicion = PosicionSerializer(read_only=True)
    status   = StatusSerializer(read_only=True)
    cantidad = serializers.SerializerMethodField()
    detalle = serializers.SerializerMethodField()

    def get_cantidad(self, obj):
        return obj.cantidad_actual_total()

    def get_detalle(self, obj):
        return obj.total_ubicaciones_detail()


    class Meta:
        model = Llanta
        fields = '__all__'


class ValeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vale
        fields = '__all__'
