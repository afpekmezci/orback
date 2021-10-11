from django.contrib import admin
from warehouse.models import Hospital, Warehouse
from import_export.admin import ImportExportModelAdmin

from import_export import resources

class HospitalResource(resources.ModelResource):
	class Meta:
		model = Hospital
		fields = ('id', 'name', 'city', 'town', 'hospital_type')
		export_order = ('name', 'city', 'town', 'hospital_type')

class HospitalAdmin(ImportExportModelAdmin):
	list_display = ['id', 'name', 'city', 'town', 'hospital_type']
	search_fields = ['name', 'city']
	resource_class = HospitalResource

admin.site.register(Hospital, HospitalAdmin)


class WarehouseAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'organization', 'city']
	

admin.site.register(Warehouse, WarehouseAdmin)