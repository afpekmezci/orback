from django.shortcuts import render
from rest_framework import generics
from base.views import FilterAPIView, DeleteAPIView, PatchAPIView
from tissue.models import TissueType, TissueMaterial
from tissue.serializers import TissueTypeSerializer, BonseMaterialSerializer
from rest_framework.permissions import IsAuthenticated
from organization.permissions import IsMainOrganization, HasOrgPermission
from tissue.permissions import TissueMaterialPermission

from django.db.models import Count, BigIntegerField, Case, When, F, Value, Q
from tissue.units import TissueStatus
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

class TissueTypeListView(FilterAPIView):
	permission_class = [HasOrgPermission]
	model =TissueType
	serializer_class = TissueTypeSerializer
	queryset = TissueType.objects.filter(is_deleted=False).all()
	search_fields = ['title', 'desc']

class AddTissueTypeView(generics.CreateAPIView):
	permission_classes = [HasOrgPermission, IsMainOrganization]
	model = TissueType
	queryset = TissueType.objects.all()
	serializer_class = TissueTypeSerializer

class UpdateTissueTypeView(generics.UpdateAPIView):
	permission_classes = [HasOrgPermission, IsMainOrganization]
	model = TissueType
	queryset = TissueType.objects.all()
	serializer_class = TissueTypeSerializer

class DeleteTissueTypeView(generics.DestroyAPIView):
	permission_classes = [HasOrgPermission, IsMainOrganization]
	model = TissueType
	queryset = TissueType.objects.all()
	serializer_class = TissueTypeSerializer

	def perform_destroy(self, instance):
		instance.is_deleted=True
		instance.save()

class AddTissueMaterial(generics.CreateAPIView):
	permission_classes = [HasOrgPermission]
	model = TissueMaterial
	queryset = TissueMaterial.objects.all()
	serializer_class = BonseMaterialSerializer

class UpdateTissueMaterial(PatchAPIView):
	permission_classes = [HasOrgPermission, TissueMaterialPermission]
	model = TissueMaterial
	queryset = TissueMaterial.objects.all()
	serializer_class = BonseMaterialSerializer

class TissueMaterialDetail(generics.RetrieveAPIView):
	permission_classes = [HasOrgPermission, TissueMaterialPermission]
	model = TissueMaterial
	queryset = TissueMaterial.objects.all()
	serializer_class = BonseMaterialSerializer

class DeleteTissueMaterial(DeleteAPIView):
	permission_classes = [HasOrgPermission, TissueMaterialPermission]
	model = TissueMaterial
	queryset = TissueMaterial.objects.all()
	serializer_class = BonseMaterialSerializer

class ListMaterialView(mixins.ListModelMixin, GenericAPIView):
	permission_classes = [HasOrgPermission, TissueMaterialPermission]
	model = TissueMaterial
	queryset = TissueMaterial.objects.filter(is_active=True, is_deleted=False)
	serializer_class = BonseMaterialSerializer

	_search = Q()
	_filter = Q()
	_detail = False
	search_fields = ['hospital__name', 'patient', 'tissue_type__name', 'organization__name']
	filter_fields = ['hospital', 'tissue_type', 'organization', 'status']
	aggregate_key = 'hospital'
	def post(self, request, *args, **kwargs):
		self.aggregate_key = self.request.data.get('aggregate', 'hospital')
		if self.request.org.main_organization:
			self.aggregate_key = 'organization'
			if self.request.data.get('filter', {}).get('organization'):
				self.aggregate_key = 'hospital'
		self.get_filter()
		self.get_queryset()
		if not self.queryset:
			return Response(status=status.HTTP_404_NOT_FOUND)
		if not self._detail:

			response = {
				'count': self.get_count(),
				'results': self.queryset,
				'aggregate_key': self.aggregate_key
			}
			return Response(response)

		page = self.paginate_queryset(self.queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			resp = self.get_paginated_response(serializer.data)
			resp.data['count'] = self.get_count(resp.data.get('results', []))
			resp.data['aggregate_key'] = self.aggregate_key
			return resp
		serializer = self.get_serializer(self.queryset, many=True)
		return Response(serializer.data)

	def get_filter(self):
		if self.request.data.get('filter'):

			for filter_fields, filter_value in self.request.data.get('filter').items():

				for model_key in self.model._meta.fields:
					if model_key.name == filter_fields and filter_value:
						if isinstance(filter_value, list):
							self._filter &= Q(**{"%s__in" % model_key.name: filter_value})
						else:
							self._filter &= Q(**{"%s" % model_key.name: filter_value})

		if hasattr(self, 'search_fields') and self.search_fields and self.request.data.get('search'):
			for item in self.search_fields:
				self._search |= Q(**{"%s__icontains" % item: self.request.data.get('search')})


	def get_annotation(self, key):
		f_key = f"{key}__name"
		return {'title': F(f_key)}

	def aggregate_queryset(self):

		self.queryset = (
			self.queryset
				.values(self.aggregate_key)
				.order_by(self.aggregate_key)
				.annotate(
					fridge=Count(
						Case(
							When(status=TissueStatus.fridge, then=1)
						)
					),
					transfer=Count(
						Case(
							When(status=TissueStatus.transfer, then=1),
							output_field=BigIntegerField(),
						),
					),
					orbone=Count(
						Case(
							When(status=TissueStatus.orbone, then=1),
							output_field=BigIntegerField(),
						),
					)
				).annotate(**self.get_annotation(self.aggregate_key))
			.order_by(self.aggregate_key))


	def get_queryset(self):
		self._detail = self.request.data.get('detail', False)
		self.queryset = self.queryset.filter(self._search, self._filter)
		if not self.request.org.main_organization:
			self.queryset = self.queryset.filter(organization__exact=self.request.org)
		if not self._detail:
			self.aggregate_queryset()

	def get_count(self, data=None):

		if self._detail:
			df = pd.DataFrame(data).groupby(['status'], as_index=True)["status"].count().to_dict()
			return df
		else:
			return {
				'orbone': sum(item['orbone'] for item in self.queryset),
				'transfer': sum(item['transfer'] for item in self.queryset),
				'fridge': sum(item['fridge'] for item in self.queryset),
			}