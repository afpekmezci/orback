from rest_framework import serializers
from files.models import BaseFileModel
from base.serializers import BaseWithCreatedBySerializer
from core.get_request import current_request
from base.fields import Base64FileField
import mimetypes
import urllib
from core.settings import API_URL


class BaseFileSerializer(BaseWithCreatedBySerializer):
	file = Base64FileField(required=True)

	def to_representation(self, instance):
		data = super(BaseFileSerializer, self).to_representation(instance)
		data['created_by_name'] = instance.created_by.name
		try:
			url = urllib.request.pathname2url(instance.file.url)
			data['mime_type'] = mimetypes.guess_type(url)[0]
			data['extension'] = mimetypes.guess_extension(data['mime_type'])
			data['extension'] = data['extension'][1:]
			data['extension'] = data['extension'].lower()
		except:
			data['mime_type'] = None
			data['extension'] = None
		data['file_url'] = f"{API_URL}servefiles{instance.file.url}"
		return data

	def create(self, validated_data):
		return super(BaseFileSerializer, self).create(validated_data)

	def update(self, instance, validated_data):
		return super(BaseFileSerializer, self).update(instance, validated_data)

	class Meta:
		model = BaseFileModel
		fields =  [
			'id', 'title', 'file', 'desc'
		] + BaseWithCreatedBySerializer.Meta.fields