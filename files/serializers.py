from rest_framework import serializers
from files.models import BaseFileModel
from base.serializers import BaseWithOrganizationSerializer
from core.get_request import current_request
from base.fields import Base64FileField
class BaseFileSerializer(BaseWithOrganizationSerializer):
	file = Base64FileField(required=True)

	def to_representation(self, instance):
		data = super(BaseFileSerializer, self).to_representation(instance)

		return data

	def create(self, validated_data):
		return super(BaseFileSerializer, self).create(validated_data)

	def update(self, instance, validated_data):
		return super(BaseFileSerializer, self).update(instance, validated_data)

	class Meta:
		model = BaseFileModel
		fields =  [
			'id', 'title', 'file', 'desc'
		] + BaseWithOrganizationSerializer.Meta.fields