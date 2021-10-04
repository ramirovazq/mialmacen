from rest_framework import serializers
from persona.models import ProfilePosition, Profile

class ProfilePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePosition
        fields = ['id'] #, 'profile', 'position']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    tipo = serializers.StringRelatedField(many=False)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'tipo']

