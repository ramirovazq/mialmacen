from django.contrib import admin
from .models import *

class MarcaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'codigo']

class MedidaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'codigo']

class PosicionAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'codigo']

class StatusAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']

class TipoMovimientoAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Medida, MedidaAdmin)
admin.site.register(Posicion, PosicionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(TipoMovimiento, TipoMovimientoAdmin)

