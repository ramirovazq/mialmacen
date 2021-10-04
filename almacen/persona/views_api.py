#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict
from .models import ProfilePosition, Profile, Tipo
from general.models import ValeAlmacenGeneral
from .serializers import ProfilePositionSerializer, ProfileSerializer
from .utils import verify_product, verify_profileposition, verify_int_quantity
from .utils import verify_profileposition_insert, prepare_data_for_movimientos
from .utils import verify_list_profileposition, verify_destino
from .utils import verify_profilepositions

class ProfilePositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)

    queryset = ProfilePosition.objects.all()
    serializer_class = ProfilePositionSerializer
    
    @action(detail=False, methods=['post'])
    def lector(self, request):
        if ('profile_position_ids' in request.data.keys()) \
            and ('destino'  in request.data.keys()) \
            and ('origen'  in request.data.keys()): # parameters: # parameters
            if isinstance(request.data, QueryDict): # this is for tests
                list_ids_profile_position = request.data.getlist('profile_position_ids')
            else: # simple dict
                list_ids_profile_position = request.data.get('profile_position_ids')
            destino_id = request.data.get('destino')
            origen_id  = request.data.get('origen')            
            if len(list_ids_profile_position) > 0 and destino_id: # is not empty the list
                set_ids_profile_position =  set(list_ids_profile_position)
                # verify if all ids are real Profile Position
                # verify if destino_id existe
                if verify_list_profileposition(set_ids_profile_position) and verify_destino(destino_id):
                    # verify if exists only one product type in each ProfilePosition
                    # group ProfilePosition: {profileposition.id: 2, profileposition.id: 1, profileposition.id: 4}
                    # verify if quantity sent for each profileposition.id is possible (really exists in warehouse)
                    result, list_results, list_productos, ids_profile_position = verify_profilepositions(list_ids_profile_position)
                    if result:
                        # if pass all verifications, create ValeGeneral in authomatic
                        # for each element in the list, create movimientogeneral
                        # ProductoExactProfilePosition.objects.create 
                        new_vale = ValeAlmacenGeneral.generate_authomatic(request.user)
                        new_vale.movimientos_authomatic_from_list_products(list_productos, origen_id, destino_id, ids_profile_position)
                        return Response({"exito":"insertado"}, status=status.HTTP_201_CREATED)
                    return Response({"error": list_results}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error":"Wrong list of profileposition ids or destino"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"List empty or destino"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['post'])
    def init(self, request):
        if ('profileposition' in request.data.keys()) \
            and ('origen'  in request.data.keys()) \
            and ('destino'  in request.data.keys()) \
            and ('product'  in request.data.keys()) \
            and ('unidad'  in request.data.keys()) \
            and ('quantity'  in request.data.keys()): # parameters: # parameters
            quantity = request.data.get('quantity')
            origen_id = request.data.get('origen')
            destino_id = request.data.get('destino')
            product_id = request.data.get('product')
            profileposition_id  = request.data.get('profileposition')
            unidad_id = request.data.get('unidad')
            
            if quantity \
                and product_id \
                and profileposition_id \
                and origen_id \
                and unidad_id \
                and destino_id: # is not empty the list
                # verify if all ids are real Profile Position
                # verify if destino_id existe
                if verify_product(product_id) \
                    and verify_profileposition(profileposition_id) \
                    and verify_destino(origen_id) \
                    and verify_destino(destino_id):
                    # verify if exists only one product type in each ProfilePosition
                    # group ProfilePosition: {profileposition.id: 2, profileposition.id: 1, profileposition.id: 4}
                    # verify if quantity sent for each profileposition.id is possible (really exists in warehouse)
                    result, list_results = verify_profileposition_insert(profileposition_id, product_id, quantity)
                    if result:
                        # if pass all verifications, create ValeGeneral in authomatic
                        # for each element in the list, create movimientogeneral
                        # ProductoExactProfilePosition.objects.create 
                        
                        new_vale = ValeAlmacenGeneral.generate_authomatic(request.user, "ENTRADA")
                        list_productos, ids_profile_position = prepare_data_for_movimientos(product_id, quantity, profileposition_id)
                        new_vale.movimientos_authomatic_from_list_products(list_productos, origen_id, destino_id, ids_profile_position, unidad_id)
                        return Response({"exito":"insertado"}, status=status.HTTP_201_CREATED)
                    return Response({"error": list_results}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error":"Wrong profileposition or product or quantity"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"Empty value"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileBodegaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)

    tipo_bodega = Tipo.objects.get(nombre="BODEGA")
    queryset = Profile.objects.filter(tipo=tipo_bodega).order_by('user__username')
    serializer_class = ProfileSerializer


class ProfileEconomicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    #permission_classes = (IsAuthenticated,)

    tipo_economico = Tipo.objects.get(nombre="ECONOMICO")
    queryset = Profile.objects.filter(tipo=tipo_economico).order_by('user__username')
    serializer_class = ProfileSerializer
