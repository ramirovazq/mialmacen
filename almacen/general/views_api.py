#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Producto, NumeroParte
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)

    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def search_product(self, request):
        productos_serializados = ProductoSerializer()
        if 'query' in request.query_params.keys():
            search = request.query_params.get('query')
            if len(search) >= 3:

                lista_productos = Producto.objects.filter(
                    nombre__icontains=search
                ).values('id')
                lista_productos = [x['id'] for x in lista_productos]

                lista_productos_np = NumeroParte.objects.filter(
                    numero_de_parte__icontains=search
                ).values('producto__id')
                lista_productos_np = [x['producto__id'] for x in lista_productos_np]

                lista_productos_suma = set(lista_productos+lista_productos_np)                
                productos = Producto.objects.filter(id__in=lista_productos_suma)
                
                productos_serializados = ProductoSerializer(productos, many=True)
        return Response(productos_serializados.data)