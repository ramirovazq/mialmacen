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

class ValeAdmin(admin.ModelAdmin):
	list_display = ['id', 'no_folio', 'tipo_movimiento', 'fecha_vale', 'con_iva', 'fecha_created', 'fecha_edited', 'persona_asociada']
	list_filter = ['tipo_movimiento']

class MovimientoAdmin(admin.ModelAdmin):
	list_display = ['id', 'vale', 'fecha_movimiento', 'origen', 'destino', 'cantidad', 'creador', 'permisionario']
	list_filter = ['permisionario']

class AdjuntoValeAdmin(admin.ModelAdmin):
	list_display = ['id', 'vale']

class LlantaAdmin(admin.ModelAdmin):
	list_display = ['id', 'marca', 'medida', 'posicion', 'status', 'dot', 'porciento_vida']

class ImportacionMovimientosAdmin(admin.ModelAdmin):
	list_display = ['id', 'fecha_created', 'procesado']


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Medida, MedidaAdmin)
admin.site.register(Posicion, PosicionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(TipoMovimiento, TipoMovimientoAdmin)
admin.site.register(Movimiento, MovimientoAdmin)
#admin.site.register(Movimiento)
admin.site.register(Vale, ValeAdmin)
admin.site.register(AdjuntoVale, AdjuntoValeAdmin)
admin.site.register(Llanta, LlantaAdmin)
admin.site.register(ImportacionMovimientos, ImportacionMovimientosAdmin)