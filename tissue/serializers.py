from rest_framework import serializers
from tissue.models import TissueType, TissueMaterial, TissueFile
from base.serializers import BaseWithOrganizationSerializer
from base.fields import TimestampField
from files.serializers import BaseFileSerializer

class TissueTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = TissueType
		fields = ['id', 'name', 'desc']


class BonseMaterialSerializer(BaseWithOrganizationSerializer):

	hospital_name = serializers.CharField(source='hospital.name', read_only=True)
	organization_name = serializers.CharField(source='organization.name', read_only=True)
	taken_time = TimestampField()
	transfer_time = TimestampField(required=False)
	delivery_time = TimestampField(required=False)
	tissue_name = serializers.CharField(source='tissue_type.name', read_only=True, required=False)
	def to_representation(self, instance):
		data = super(BonseMaterialSerializer, self).to_representation(instance)
		data['file_count'] = instance.tissue_files.count()
		return data

	def update(self, instance, validated_data):
		return super(BonseMaterialSerializer, self).update(instance, validated_data)
	class Meta:
		model = TissueMaterial
		fields = BaseWithOrganizationSerializer.Meta.fields + [
			'id',
			'tissue_type',
			'tissue_name',
			'patient',
			'hospital',
			'hospital_name',
			'organization_name',
			'status',
			'taken_time',
			'transfer_time',
			'delivery_time'
		]


class TissueFileSerializer(BaseFileSerializer):
	date = TimestampField()
	class Meta:
		model = TissueFile
		fields = BaseFileSerializer.Meta.fields + ['tissue', 'date']