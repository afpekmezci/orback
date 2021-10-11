from rest_framework import serializers
from supplier.models import Supplier
from base.serializers import BaseSerializer


class SupplierSerializer(BaseSerializer):

	class Meta:
		model = Supplier
		fields = ['created_by', 'company']