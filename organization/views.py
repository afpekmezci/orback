from django.shortcuts import render
from rest_framework import generics
from organization.models import Organization, OrganizationUser, OrganizationOwner
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from base.views import FilterAPIView
from organization.permissions import IsOwnerOrReadOnly, IsMainOrganization, IsOrgPersonelOrgMainOrg, HasOrgPermission

from django.db.models import Q

class CreateOrganizationView(generics.CreateAPIView):
	permission_classes = (HasOrgPermission, IsMainOrganization)
	model = Organization
	queryset = model.objects.none()
	serializer_class = OrganizationSerializer

class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (HasOrgPermission, IsOwnerOrReadOnly)
	model = Organization
	queryset = model.objects.filter(is_deleted=False).all()
	serializer_class = OrganizationSerializer

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save()

class OrganizationListView(generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	model = Organization
	queryset = model.objects.all()
	serializer_class = OrganizationSerializer
	search_fields = ['name']

	def get_queryset(self):
		return self.queryset.filter(user_organizatons__user__in=[self.request.user])

class SupplierListView(FilterAPIView):

	permission_classes = (HasOrgPermission, IsMainOrganization)
	model = Organization
	queryset = model.objects.all()
	serializer_class = OrganizationSerializer
	search_fields = ['name', 'city']
	filter_fields = ['is_active', 'organization']
	order_by = 'name'


class AddUserToOrganizationView(generics.CreateAPIView):
	permission_classes = (HasOrgPermission, IsOwnerOrReadOnly)
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer
	def get_serializer_class(self):
		self.request.data['organization'] = self.request.org.id
		return super(AddUserToOrganizationView, self).get_serializer_class()

class RemoveUserFromOrganization(generics.DestroyAPIView):
	permission_classes = (HasOrgPermission, IsOwnerOrReadOnly)
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer

	def perform_destroy(self, instance):
		instance.is_active = False
		instance.save()

class OrganizationUserList(FilterAPIView):

	permission_classes = (HasOrgPermission, IsOwnerOrReadOnly)
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer
	search_fields = ['user__name', 'user__email']
	filter_fields = ['is_active', 'organization']

	def get_queryset(self):
		_filter = Q(organization__exact=self.request.org)
		if (
			self.request.org.main_organization and
			(
				self.request.data.get('filter', {}).get('show_all') or
				self.request.data.get('filter', {}).get('organization')
			)
		):
			_filter = Q()
		return self.queryset.filter(_filter)


