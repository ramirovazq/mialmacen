from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import *
from persona.models import Profile, Tipo

from .serializers import ValeSerializer, LlantaSerializer, ProfileSerializer
from .serializers import MovimientoSerializer, MarcaLlantaSerializer
from .serializers import LlantaSpecificSerializer

## curl -X GET http://127.0.0.1:8000/api/v0/vale/ -H 'Authorization: Token ABCDEF343434342234234KMLMKMLKM'
class MovimientoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Movimiento.objects.all().order_by('-date_created')
    serializer_class = MovimientoSerializer


class ValeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Vale.objects.all().order_by('-fecha_created')
    serializer_class = ValeSerializer


    def perform_create(self, serializer):
        if not 'no_folio' in serializer.validated_data.keys():
            vale = serializer.save(no_folio=Vale.siguiente_folio())
        else:
            vale = serializer.save()


class LlantaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Llanta.objects.all()
    serializer_class = LlantaSpecificSerializer


class EconomicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    #obj_tipo, bandera = Tipo.objects.get_or_create(nombre="ECONOMICO")
    #queryset = Profile.objects.filter(tipo=obj_tipo)
    #serializer_class = ProfileSerializer


