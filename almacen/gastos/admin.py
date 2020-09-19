from django.contrib import admin
from .models import *

class CategoriaGastosAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria']
    list_filter = ['categoria']
    search_fields = ['categoria']

class GastoAdmin(admin.ModelAdmin):
    list_display = ['id', 'concepto', 'monto', 'fecha_created', 'fecha', 'perdida']
    list_filter = ['perdida']
    search_fields = ['concepto']


admin.site.register(CategoriaGastos, CategoriaGastosAdmin)
admin.site.register(Gasto, GastoAdmin)