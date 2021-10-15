from django.contrib import admin

from organization.models import Organization, OrganizationUser, OrganizationOwner

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'main_organization']
admin.site.register(OrganizationUser)
admin.site.register(OrganizationOwner)