from rest_framework import serializers
from persona.models import ProfilePosition

class ProfilePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePosition
        fields = ['id'] #, 'profile', 'position']

'''
from rest_framework import serializers
from persona.models import ProfilePosition
class ProfilePositionSerializer(serializers.ModelSerializer):
     class Meta:
         model = ProfilePosition
         fields = ['id']
         #fields = ['id', 'profile', 'position']
pp = ProfilePosition.objects.all()[0]
s = ProfilePositionSerializer(pp)
s.data
{'id': 1, 'profile': 144, 'position': 2}
ProfilePositionSerializer(ProfilePosition.objects.all(), many=True)
ids_pp = ProfilePosition.objects.all().values_list('id')
'''