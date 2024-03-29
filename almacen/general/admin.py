from django.contrib import admin
from .models import *
from shared.models import ExportCsvMixin

class NumeroParteAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id', 'producto', 'numero_de_parte']
    search_fields = ['producto__nombre', 'numero_de_parte']
    actions = ["export_as_csv"]


class ProductoAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['id', 'nombre', 'minimum', 'maximum']
    search_fields = ['nombre']
    actions = ["export_as_csv"]

class ValeAlmacenGeneralAdmin(admin.ModelAdmin):
    list_display = ['id', 'no_folio', 'tipo_movimiento', 'fecha_vale', 'con_iva', 'fecha_created', 'fecha_edited', 'persona_asociada', 'vale_llantas']
    list_filter = ['tipo_movimiento', 'vale_llantas']

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
admin.site.register(NumeroParte, NumeroParteAdmin)