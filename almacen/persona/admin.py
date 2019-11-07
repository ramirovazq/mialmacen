from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tipo']
    search_fields = ['user__username']

class TipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']

class ProfilePositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'position']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ProfilePosition, ProfilePositionAdmin)



# Register your models here.
