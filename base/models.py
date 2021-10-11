from django.db import models


class BaseModel(models.Model):
	created_time = models.DateTimeField(auto_now=True)
	update_time = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	class Meta:
		abstract = True
