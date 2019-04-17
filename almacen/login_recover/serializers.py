from rest_framework import serializers
#from .models import Staff
#from oauth2_provider.models import Application
#from oauth2_provider.models import AccessToken
#from django.utils import timezone

'''
class WhoisSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200, required=True)
    def validate_token(self, value):
      try:
        t = AccessToken.objects.get(token=value)
        ahora = timezone.now()
        if (ahora > t.expires):
          raise serializers.ValidationError('Token no valido')
      except AccessToken.DoesNotExist:
        raise serializers.ValidationError('Token no valido')
      return value
'''

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200, required=True)
