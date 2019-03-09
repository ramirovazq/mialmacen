from django.contrib import admin
from .models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
	list_display = ['vehicle_model', 'vehicle_make', 'color', 'doors', 'lot_number']
	list_filter =  ['vehicle_make', 'color', 'doors']
	search_fields = ['vehicle_model', 'vehicle_make', 'color', 'lot_number']
	
	fieldsets = (
        (None, {
            'fields': (('vehicle_make','vehicle_model'),
            		   'description',
            		   ('color','doors','lot_number')
            		   ),
        }),
     )
	

admin.site.register(Vehicle, VehicleAdmin)
admin.site.site_header = "Vehicle Inventory"