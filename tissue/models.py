from django.db import models
from base.models import BaseModel, BaseModelWithOrganization
from tissue.units import TissueStatus


class TissueType(BaseModel):

	title = models.CharField(verbose_name='Title', max_length=128)
	desc = models.CharField(verbose_name='Description', max_length=2048, blank=True, null=True)

	def __str__(self):
		return self.title


class TissueMaterial(BaseModelWithOrganization):
	tissue_type = models.ForeignKey(TissueType, on_delete=models.CASCADE, verbose_name='Tissue Type', related_name='tissue_materials')
	patient = models.CharField(verbose_name='Patient', max_length=128, blank=True, null=True)
	hospital = models.ForeignKey('warehouse.hospital', on_delete=models.PROTECT, verbose_name='Hospital', related_name='hospital_tissues')
	status = models.CharField(choices=TissueStatus().get_list(), default=TissueStatus.fridge, max_length=48)
	taken_time = models.DateTimeField(auto_now=False, verbose_name='Taken Time')
	transfer_time = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name='Transfer Time')
	delivery_time = models.DateTimeField(blank=True, null=True, auto_now=False, verbose_name='Delivery Time')
	def __str__(self):
		return f"{self.tissue_type} {self.organization} {self.hospital}"