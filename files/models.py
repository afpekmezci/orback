from django.db import models
from core.settings import AUTH_USER_MODEL
from base.models import BaseModel
from core.utils import get_upload_path


class BaseFileModel(BaseModel):

	created_by = models.ForeignKey(
		AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		verbose_name="Created By",
		related_name="user_files",
	)

	title = models.CharField(verbose_name="Title", max_length=128)

	file = models.FileField(upload_to=get_upload_path)

	desc = models.TextField(verbose_name='Description', blank=True, null=True)

	def __str__(self):
		return f"{self.title}"

	class Meta:
		abstract=True
