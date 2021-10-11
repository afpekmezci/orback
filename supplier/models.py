from django.db import models
from base.models import BaseModel

class Supplier(BaseModel):
	created_by=models.ForeignKey('customuser.User', on_delete=models.PROTECT, verbose_name='Created By')
	employer=models.ForeignKey('organization.organization', on_delete=models.PROTECT, verbose_name='Organizations')
	supplier=models.ForeignKey('organization.organization', on_delete=models.PROTECT, verbose_name='Supplier', related_name='suppliers')

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['employer', 'supplier'], name="supplier-unique")
		]