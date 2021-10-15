from rest_framework import serializers
from tissue.models import TissueType, TissueMaterial
from base.serializers import BaseWithOrganizationSerializer
from base.fields import TimestampField

class TissueTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = TissueType
		fields = ['id', 'title', 'desc']


class BonseMaterialSerializer(BaseWithOrganizationSerializer):

	hospital_name = serializers.CharField(source='hospital.name', read_only=True)
	organization_name = serializers.CharField(source='organization.name', read_only=True)
	taken_time = TimestampField()
	transfer_time = TimestampField(required=False)
	delivery_time = TimestampField(required=False)
	tissue_title = serializers.CharField(source='tissue_type.title', read_only=True, required=False)
	def to_representation(self, instance):
		data = super(BonseMaterialSerializer, self).to_representation(instance)

		return data
	class Meta:
		model = TissueMaterial
		fields = BaseWithOrganizationSerializer.Meta.fields + [
			'id',
			'tissue_type',
			'tissue_title',
			'patient',
			'hospital',
			'hospital_name',
			'organization_name',
			'status',
			'taken_time',
			'transfer_time',
			'delivery_time'
		]
