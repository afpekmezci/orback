from django.db import models
from base.models import BaseModel

class Hospital(BaseModel):

	name = models.CharField(verbose_name='Hospital', max_length=1024)
	city = models.CharField(verbose_name='City', max_length=128, blank=True, null=True)
	town = models.CharField(verbose_name='Town', max_length=128, blank=True, null=True)
	hospital_type = models.CharField(verbose_name='Type', max_length=128, blank=True, null=True)

	def __str__(self):
		return f"{self.name} {self.city}"
	
class Warehouse(BaseModel):
	name = models.CharField(verbose_name='Warehouse Name', max_length=128)
	city = models.CharField(verbose_name='City', max_length=128, blank=True, null=True)
	organization = models.ForeignKey('organization.organization', on_delete=models.PROTECT, related_name='warehouses')