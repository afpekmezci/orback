from django.contrib import admin

from organization.models import Organization, OrganizationUser, OrganizationOwner

admin.site.register(Organization)
admin.site.register(OrganizationUser)
admin.site.register(OrganizationOwner)