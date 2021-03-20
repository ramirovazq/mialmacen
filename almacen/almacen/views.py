from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from django.contrib.auth.models import User, Group
#from oauth2_provider.models import Application

from django.views.generic import View

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger import renderers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.core.files.storage import default_storage
import mimetypes


def index(request):
    context = {}
    return render(request, 'index_fletes.html', context)


class SwaggerSchemaView(APIView):
        #exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer,
            CoreJSONRenderer,
        ]
        authentication_classes = [TokenAuthentication, SessionAuthentication]

        def get(self, request):
                generator = SchemaGenerator(title='Fletes API')
                # Show protected endpoints by bypassing auth setting
                schema = generator.get_schema()

                return Response(schema)
