from rest_framework import serializers
from warehouse.models import Hospital


class HospitalSerializer(serializers.ModelSerializer):

	class Meta:
		model = Hospital
		fields = ['id', 'name', 'city']
