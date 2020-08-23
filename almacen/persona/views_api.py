#from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ProfilePosition
from .serializers import ProfilePositionSerializer
from .utils import verify_list_profileposition, verify_destino, verify_profilepositions

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
        if ('profile_position_ids' in request.data.keys()) and ('destino'  in request.data.keys()): # parameters: # parameters
            list_ids_profile_position = request.data.getlist('profile_position_ids')
            destino_id = request.data.get('destino')            
            if len(list_ids_profile_position) > 0 and destino_id: # is not empty the list
                set_ids_profile_position =  set(list_ids_profile_position)
                # verify if all ids are real Profile Position
                # verify if destino_id existe
                if verify_list_profileposition(set_ids_profile_position) and verify_destino(destino_id):
                    # verify if exists only one product type in each ProfilePosition
                    # group ProfilePosition: {profileposition.id: 2, profileposition.id: 1, profileposition.id: 4}
                    # verify if quantity sent for each profileposition.id is possible (really exists in warehouse)
                    result, list_results = verify_profilepositions(list_ids_profile_position)
                    if result:
                        print("...... COOL .....")
                        # if pass all verifications, create ValeGeneral in authomatic
                        # for each element in the list, create movimientogeneral
                        # ProductoExactProfilePosition.objects.create 
                        return Response({"exito":"cool"}, status=status.HTTP_201_CREATED)
                    return Response({"error": list_results}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"error":"Wrong list of profileposition ids or destino"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"List empty or destino"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
