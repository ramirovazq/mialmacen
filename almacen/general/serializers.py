from rest_framework import serializers
from general.models import Producto, NumeroParte
#from persona.models import Profile, Tipo
class NumeroParteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeroParte
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    numeros_de_parte = NumeroParteSerializer(many=True, read_only=True)
    position = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()

    def get_position(self, obj):
        return obj.what_in_positions_inventory_specific()


    def get_inventory(self, obj):
        #print('specific_position...... ini')
        #print(obj.what_in_positions_inventory_specific_obj())
        #print('specific_position...... fin')
        return obj.inventory_words()


    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'position',
            'inventory',
            'numeros_de_parte'
            ]
'''
class ProfileSerializer(serializers.ModelSerializer):
    tipo    = TipoSerializer(read_only=True)
    nombre = serializers.SerializerMethodField()

    def get_nombre(self, obj):
        print(obj.user.username)
        return obj.user.username

    class Meta:
        model = Profile
        fields = '__all__'


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
        return obj.total_ubicaciones_detail_endpoint()


    class Meta:
        model = Llanta
        fields = '__all__'


class ValeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vale
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'
'''