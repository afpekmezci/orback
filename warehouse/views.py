from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from warehouse.models import Hospital
from warehouse.serializers import HospitalSerializer
from base.views import FilterAPIView
from organization.permissions import IsOwnerOrReadOnly, IsMainOrganization, IsOrgPersonelOrgMainOrg, HasOrgPermission

class CreateHospitalView(generics.CreateAPIView):
	model = Hospital
	permission_classes = (HasOrgPermission,)
	serializer_class = HospitalSerializer
	queryset = model.objects.all()


class ListHospitalView(FilterAPIView):
	model = Hospital
	permission_classes = (HasOrgPermission, )
	serializer_class = HospitalSerializer
	queryset = model.objects.all()
	search_fields = ['name', 'city']
	

class UpdateHospitalView(generics.UpdateAPIView):
	model = Hospital
	permission_classes = (HasOrgPermission, )
	serializer_class = HospitalSerializer
	queryset = model.objects.all()


class DeleteHospitalView(generics.DestroyAPIView):
	model = Hospital
	permission_classes = (HasOrgPermission, IsMainOrganization)
	serializer_class = HospitalSerializer
	queryset = model.objects.all()

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save()