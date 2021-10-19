from django.contrib import admin
from tissue.models import TissueType, TissueMaterial, TissueFile


@admin.register(TissueType)
class BoneTypeAdmin(admin.ModelAdmin):
	list_display = ['pk', 'name', 'desc']


@admin.register(TissueMaterial)
class BoneMaterialAdmin(admin.ModelAdmin):
	list_display = ['pk', 'organization', 'status']

@admin.register(TissueFile)
class TissueFileAdmin(admin.ModelAdmin):
	list_display = ["pk", "tissue", "title" ,"is_deleted"]