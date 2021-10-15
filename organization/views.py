from django.shortcuts import render
from rest_framework import generics
from organization.models import Organization, OrganizationUser, OrganizationOwner, OrganizationFile
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer, OrganizationFileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from base.views import FilterAPIView
from organization.permissions import IsOwnerOrReadOnly, IsMainOrganization, IsOrgPersonelOrgMainOrg, HasOrgPermission
from files.views import (
	FileDetailView,
	CreateFileView,
	ListFileView,
	UpdateFileView,
	DeleteFileView
)

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

	def get_queryset(self):

		print('QUERYSET : ' , self.queryset)

		return self.queryset.filter(organization__exact=self.request.org)


class OrganizationFileList(FilterAPIView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()
	search_fields = ['name', 'desc', 'organization__name']
	filter_fields = ['organization']
	def get_queryset(self):
		super(OrganizationFileList, self).get_queryset()
		queryset = self.queryset
		if not self.request.org.main_organization:
			queryset = self.queryset.filter(organization__exact=self.request.org)
		return queryset
class OrganizationFileCreate(CreateFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileDetail(FileDetailView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileUpdate(UpdateFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileDelete(DeleteFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()
