from django.shortcuts import render
from rest_framework import generics
from organization.models import Organization, OrganizationUser, OrganizationOwner
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from base.views import FilterAPIView


class CreateOrganizationView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
	model = Organization
	queryset = model.objects.none()
	serializer_class = OrganizationSerializer

class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticated]
	model = Organization
	queryset = model.objects.all()
	serializer_class = OrganizationSerializer

class OrganizationListView(FilterAPIView):
	permission_classes = [IsAuthenticated]
	model = Organization
	queryset = model.objects.all()
	serializer_class = OrganizationSerializer
	search_fields = ['name']

class AddUserToOrganizationView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer

class RemoveUserFromOrganization(generics.DestroyAPIView):
	permission_classes = [IsAuthenticated]
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer

	def perform_destroy(self, instance):
		instance.is_active = False
		instance.save()

class OrganizationUserList(FilterAPIView):

	permission_classes = [IsAuthenticated]
	model = OrganizationUser
	queryset = model.objects.all()
	serializer_class = OrganizationUserSerializer
	search_fields = ['user__name', 'user__email']


