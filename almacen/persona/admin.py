from django.contrib import admin
from .models import Profile, Tipo

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'tipo']

class TipoAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tipo, TipoAdmin)



# Register your models here.
