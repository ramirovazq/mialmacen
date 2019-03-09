from django.contrib import admin
from .models import Clasificacion

class ClasificacionAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']


admin.site.register(Clasificacion, ClasificacionAdmin)

