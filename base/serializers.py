from rest_framework import serializers
from base.utils import can_edit
from core.get_request import current_request


class BaseSerializer(serializers.ModelSerializer):

	class Meta:
		abstract=True
		fields = ['created_time', 'update_time']


class BaseWithCreatedBySerializer(serializers.ModelSerializer):
	created_by_name = serializers.CharField(source='created_by__name', read_only=True, required=False)
	can_edit = serializers.SerializerMethodField()
	def get_can_edit(self, obj):
		request = current_request()
		return True #can_edit(obj, request)
	def to_internal_value(self, data):
		data['created_by'] = current_request().user.id
		return super(BaseWithCreatedBySerializer, self).to_internal_value(data)
	class Meta:
		abstract=True
		fields = ['created_time', 'update_time', 'created_by', 'can_edit', 'created_by_name']


class BaseWithOrganizationSerializer(BaseWithCreatedBySerializer):
	organization_name = serializers.CharField(source='organization__name', read_only=True, required=False)
	def to_internal_value(self, data):
		print('Status : ', self.partial)
		if not self.partial:
			if not data.get('organization'):
				_org = current_request().org
				if _org:
					data['organization'] = current_request().org.id
		return super(BaseWithOrganizationSerializer, self).to_internal_value(data)
	class Meta:
		abstract=True
		fields =BaseWithCreatedBySerializer.Meta.fields +  ['organization']
