from django.db import models
from base.models import BaseModel
from bone.units import BoneStatus
class BoneType(BaseModel):

	title = models.CharField(verbose_name='Title', max_length=128)
	desc = models.CharField(verbose_name='Description', max_length=2048, blank=True, null=True)

class BoneMaterial(BaseModel):

	taken_by = models.ForeignKey('customuser.User', verbose_name='Taken By', on_delete=models.PROTECT)
	organization = models.ForeignKey('organization.organization', verbose_name='Organization', on_delete=models.PROTECT)
	taken_from = models.CharField(verbose_name='Patient', max_length=128, blank=True, null=True)
	hospital = models.ForeignKey('warehouse.hospital', on_delete=models.PROTECT, verbose_name='Hospital')
	status = models.CharField(choices=BoneStatus().get_list(), default=BoneStatus.fridge, max_length=48)

