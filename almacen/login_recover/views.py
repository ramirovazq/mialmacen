from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate

from rest_framework import viewsets

from .models import *
from .serializers import LoginSerializer

from rest_framework.permissions import AllowAny
from rest_framework import generics, status
#from apps.permissions.permissions import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

#import apps.staff.querysets
#from apps.shared.querysets import get_model_queryset_by_user
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class Login(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        s = LoginSerializer(data=request.data)
        if s.is_valid():
            try:
                user = authenticate(
                    username=s.data['username'],
                    password=s.data['password']
                )
            except Exception as e:
                content = {'error': str(e)}
                return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user is not None:
                #client = Application.objects.get(user=user)
                username = s.validated_data['username']
                user = User.objects.get(username=username)
                try:
                    # user already verified exist
                    token, bandera_token = Token.objects.get_or_create(user=user)
                    response_data = {
                        'token': token.key,
                        'email': user.email,
                        'user_id': user.id
                    }
                except Token.DoesNotExist:
                    return Response({'error': 'Error'},
                                status=status.HTTP_404_NOT_FOUND)    
                return Response(response_data)
            else:
                return Response({'error': 'Wrong username or password'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
