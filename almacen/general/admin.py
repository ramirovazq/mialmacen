from django.contrib import admin
from .models import *

class ProductoAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']


class ValeAlmacenGeneralAdmin(admin.ModelAdmin):
	list_display = ['id', 'no_folio', 'tipo_movimiento', 'fecha_vale', 'con_iva', 'fecha_created', 'fecha_edited', 'persona_asociada']
	list_filter = ['tipo_movimiento']

class MovimientoGeneralAdmin(admin.ModelAdmin):
	list_display = ['id', 'vale', 'fecha_movimiento', 'origen', 'destino', 'cantidad', 'creador', 'producto', 'unidad']

class TipoUnidadMedidaAdmin(admin.ModelAdmin):
	list_display = ['id', 'tipo']

class CategoriaUnidadMedidaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']

class UnidadMedidaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'categoria', 'tipo_unidad', 'ratio', 'simbolo']

class ProductoExactProfilePositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'exactposition', 'movimiento']

admin.site.register(TipoUnidadMedida, TipoUnidadMedidaAdmin)
admin.site.register(CategoriaUnidadMedida, CategoriaUnidadMedidaAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)

admin.site.register(Producto, ProductoAdmin)
admin.site.register(ValeAlmacenGeneral, ValeAlmacenGeneralAdmin)
admin.site.register(MovimientoGeneral, MovimientoGeneralAdmin)
admin.site.register(ProductoExactProfilePosition, ProductoExactProfilePositionAdmin)