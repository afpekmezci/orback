from django.db import models


class BaseModel(models.Model):
	created_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	class Meta:
		abstract = True


class BaseModelWithOrganization(BaseModel):

	created_by = models.ForeignKey('customuser.User', verbose_name='Taken By', on_delete=models.PROTECT, related_name='bones_taken_by')
	organization = models.ForeignKey('organization.organization', verbose_name='Organization', on_delete=models.PROTECT, related_name='organization_bones')
	class Meta:
		abstract = True