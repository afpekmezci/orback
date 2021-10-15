from django.contrib import admin
from tissue.models import TissueType, TissueMaterial


@admin.register(TissueType)
class BoneTypeAdmin(admin.ModelAdmin):
	list_display = ['pk', 'title', 'desc']


@admin.register(TissueMaterial)
class BoneMaterialAdmin(admin.ModelAdmin):
	list_display = ['pk', 'organization', 'status']